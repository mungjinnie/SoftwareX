import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision.datasets as dset
import torchvision.transforms as T
from torch.utils.data import DataLoader
from torch.utils.data import sampler
import matplotlib.pyplot as plt
import os
import copy
import pandas as pd
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics.pairwise import cosine_similarity
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dtype = torch.long
import random
from einops import rearrange, repeat, reduce
from einops.layers.torch import Rearrange

from pytorch_transformers.optimization import WarmupCosineSchedule
import cv2

from torchvision import datasets
from PIL import Image
import requests
import boto3
from botocore.client import Config
from ququ.models import *

resize_train_mean=[0.84079, 0.81977236, 0.8120078]
resize_train_std=[0.26350775, 0.28762895, 0.2983056]

resize_test_mean=[0.84397084, 0.8255839, 0.81870157]
resize_test_std=[0.26283526, 0.28287607, 0.29242957]

ss_imagenet_labels = {'bohemian_feminine': 0,
 'casual_simple': 1,
 'chic_elegance': 2,
 'dark_punk': 3,
 'elegance': 4,
 'feminine_grunge': 5,
 'formal': 6,
 'hip_hop': 7,
 'oversized_grunge': 8,
 'pure_feminine': 9,
 'sexy_chic': 10,
 'sexy_feminine': 11,
 'street_casual': 12,
 'street_punk': 13,
 'vivid_punk': 14}

fw_imagenet_labels = {'basic_casual': 0,
 'bohemian_elegance': 1,
 'chic_formal': 2,
 'chic_grunge': 3,
 'cozy_casual': 4,
 'dark_romance': 5,
 'elegance': 6,
 'feminine_casual': 7,
 'formal': 8,
 'hip_hop': 9,
 'rock_chic': 10,
 'sexy_feminine': 11,
 'sexy_street': 12,
 'tomboy': 13,
 'vintage_street': 14}

class MultiHeadAttentionLayer(nn.Module):
    def __init__(self, d_model, nhead, dropout_ratio):
        super().__init__()

        self.d_model = d_model # d_model : embed dimension
        self.nhead = nhead # nhead : head 수
        self.head_dim = d_model // nhead # head_dim : head 마다의 dimension
        self.qLinear = nn.Linear(d_model, d_model) # query lineqr
        self.kLinear = nn.Linear(d_model, d_model) # key linear
        self.vLinear = nn.Linear(d_model, d_model) # value linear

        self.oLinear = nn.Linear(d_model, d_model) # output linear

        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self, query, key, value): 

        batch_size = query.shape[0]
        query_len = query.shape[1]
        value_len = key_len = key.shape[1]

 
        Q = self.qLinear(query)
        K = self.kLinear(key)
        V = self.vLinear(value)

        Q = rearrange(Q, 'b l (h d) -> b h l d', h=self.nhead)
        K = rearrange(K, 'b l (h d) -> b h l d', h=self.nhead)
        V = rearrange(V, 'b l (h d) -> b h l d', h=self.nhead)


        weight = torch.matmul(Q, rearrange(K, 'b h l d -> b h d l')) / np.sqrt(self.head_dim)


        attention = torch.softmax(weight, dim=-1)


        c = torch.matmul(self.dropout(attention), V)


        c = rearrange(c, 'b h l d -> b l (h d)')


        output = self.oLinear(c)


        return output, attention

class PositionWiseFeedForwardLayer(nn.Module):
    def __init__(self, d_model, ff_dim, dropout_ratio):
        super().__init__()
        self.linear1 = nn.Linear(d_model, ff_dim)
        self.linear2 = nn.Linear(ff_dim, d_model)

        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self, x):


        x = self.dropout(nn.functional.gelu(self.linear1(x)))


        x = self.linear2(x)


        return x

class EncoderLayer(nn.Module):
    def __init__(self, d_model, nhead, ff_dim, dropout_ratio):
        super().__init__()

        self.layerNorm1 = nn.LayerNorm(d_model)
        self.layerNorm2 = nn.LayerNorm(d_model)
        self.multiHeadAttentionLayer = MultiHeadAttentionLayer(d_model, nhead, dropout_ratio)
        self.positionWiseFeedForward = PositionWiseFeedForwardLayer(d_model, ff_dim, dropout_ratio)
        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self, src):

        _src = self.layerNorm1(src)

        _src, attention = self.multiHeadAttentionLayer(_src, _src, _src)

        src = src + self.dropout(_src)

        _src = self.layerNorm2(src)

        # src: [batch_size, src_len, d_model]

        _src = self.positionWiseFeedForward(_src)

        src = src + self.dropout(_src)

        # src: [batch_size, src_len, d_model]

        return src, attention

class Encoder(nn.Module):
    def __init__(self, d_model, n_layers, nhead, ff_dim, dropout_ratio):
        super().__init__()

        self.layers = nn.ModuleList([EncoderLayer(d_model, nhead, ff_dim, dropout_ratio) for _ in range(n_layers)])

    def forward(self, src):

        # src: [batch_size, src_len, d_model]

        for layer in self.layers:
            src, attention = layer(src)

        # src: [batch_size, src_len, d_model]

        return src, attention

class ImageEmbedding(nn.Module):
    def __init__(self, channel, patch_size, D):
        super().__init__()
        self.rearrange = Rearrange('b c (num_w p1) (num_h p2) -> b (num_w num_h) (p1 p2 c) ', p1=patch_size, p2=patch_size)
        self.linear = nn.Linear(channel*patch_size*patch_size, D)
        # learnable cls_token (only for classification)
        self.cls_token = nn.Parameter(torch.randn(1, 1, D))

    def forward(self, image):

        b, c, w, h = image.shape

        flatten_patches = self.rearrange(image)


        embedded_patches = self.linear(flatten_patches)

        cls_tokens = repeat(self.cls_token, 'b n d -> (b repeat) n d', repeat=b)
        embedded_patches = torch.cat((cls_tokens, embedded_patches), dim=1)


        return embedded_patches

class TokPosEmbedding(nn.Module):
    def __init__(self, c, p, d_model, dropout_ratio):
        super().__init__()
        self.tokEmbedding = ImageEmbedding(c, p, d_model)
        self.posEmbedding = nn.Embedding(100, d_model) 
        self.d_model = d_model
        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self, src):

        # src: [batch_size, width, height, channel]

        src = self.tokEmbedding(src)

        # src: [batch_size, src_len, d_model]

        batch_size = src.shape[0]
        src_len = src.shape[1]

        pos = torch.arange(0, src_len, dtype=dtype) # pos: [src_len]
        pos = repeat(pos, 'l -> b l', b=batch_size).to(device) # pos: [batch_size, src_len]

        src = self.dropout(src * float(np.sqrt(self.d_model)) + self.posEmbedding(pos))
        # Dropout, when used, is applied after every dense layer except for the the qkv-projections and directly after adding positional- to patch embeddings

        # src: [batch_size, src_len, d_model]

        return src

class VisionTransformer(nn.Module):
    def __init__(self, c, p, d_model, n_layers, nhead, ff_dim, dropout_ratio, output_dim):
        super().__init__()

        self.encEmbedding = TokPosEmbedding(c, p, d_model, dropout_ratio)
        self.encoder = Encoder(d_model, n_layers, nhead, ff_dim, dropout_ratio)
        self.layerNorm = nn.LayerNorm(d_model)
        self.linear = nn.Linear(d_model, output_dim) 

    def forward(self, src):
        
        # image: [batch_size, channel, width, height]

        src = self.encEmbedding(src)

        # src: [batch_size, src_len, d_model]

        enc_src, attention = self.encoder(src)

        # enc_src: [batch_size, src_len, d_model] # encoder의 출력값.

        # classification head

        enc_src = enc_src[:,0,:] # cls tokken

        # enc_src: [batch_size, d_model]

        enc_src = self.layerNorm(enc_src)

        output = self.linear(enc_src)

        # output: [batch_size, output_dim]

        return output, attention, enc_src

def trainer(model_name, model, criterion, optimizer, scheduler, num_epochs):

    model.to(device)
    writer = SummaryWriter(f'runs/{model_name}')
    best_model_wts = copy.deepcopy(model.state_dict())
    global_step, best_acc = 0, 0.0
    running_loss, running_acc = {}, {}

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss[phase], running_acc[phase] = 0.0, 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs, _, __ = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss[phase] += loss.item() * inputs.shape[0]
                running_acc[phase] += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()
            
            running_loss[phase] = running_loss[phase] / (len(dataloaders[phase]) * dataloaders[phase].batch_size)
            running_acc[phase] = running_acc[phase].double() / (len(dataloaders[phase]) * dataloaders[phase].batch_size)

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, running_loss[phase], running_acc[phase]))
            
            # deep copy the model
            if phase == 'val' and running_acc[phase] > best_acc:
                best_acc = running_acc[phase]
                best_model_wts = copy.deepcopy(model.state_dict())

        writer.add_scalars(f'{model_name}/loss', {'train' : running_loss['train'], 'val' : running_loss['val']}, global_step)
        writer.add_scalars(f'{model_name}/acc', {'train' : running_acc['train'], 'val' : running_acc['val']}, global_step)
        writer.add_scalar(f'{model_name}/lr', scheduler.get_last_lr()[0], global_step)
        global_step += 1
        
        torch.save(model, '{}_{}.pth'.format('epoch',epoch))
        
        print()

    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)

    torch.save(model.state_dict(), f'{model_name}.pt')
    print('model saved')

    writer.close()

    return model

def checker(loader, model):

    model.eval()
    with torch.no_grad():
        correct_num = 0
        for iters, (batch_x, batch_t) in enumerate(loader):

            batch_x = batch_x.to(device)
            batch_t = batch_t.to(device)

            predict, _ = model(batch_x)
            _, predict = predict.max(1)

            correct_num += (predict == batch_t).sum()
        
    return correct_num
def normalization(x):
    min_value = min(x)
    max_value = max(x) 

    return list(map(lambda x: (x-min_value)/(max_value-min_value), x))

def style_classification(url, season, global_user_name, ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME):
    global resize_test_mean, resize_test_std
    asdf = random.randrange(1,10000)
    channel = 3
    patch_size = 4
    d_model = 128
    n_layers = 6
    nhead = 4
    ff_dim = 1024
    dropout_ratio = 0.2
    output_dim = 15
    model = VisionTransformer(channel, patch_size, d_model, n_layers, nhead, ff_dim, dropout_ratio, output_dim)
    model.load_state_dict(torch.load(f"./ququ/apicode/Transformer/23{season}.pt"))
    model = model.eval()
    model = model.to(device)
    if season =="ss":
        global ss_imagenet_labels
        imagenet_labels = ss_imagenet_labels
    elif season =="fw":
        global fw_imagenet_labels
        imagenet_labels = fw_imagenet_labels
    imagenet_labels = {v:k for k,v in imagenet_labels.items()}
    transform = T.Compose([
            T.Resize((32, 32)),
            T.ToTensor(),
            T.Normalize(resize_test_mean, resize_test_std)
            ])

    image = Image.open(requests.get(url, stream=True).raw)
    img_tensor = transform(image)
    logits, att_mat, t = model(img_tensor.unsqueeze(0).to(device, torch.float))
    new_logits = torch.tensor([normalization(logits.tolist()[0])])

    top5 = torch.argsort(new_logits, dim=-1, descending=True)
    sums = 0
    for idx in top5[0, :]:
        sums += round(new_logits[0, idx.item()].item() + new_logits[0, top5[0, -1].item()].item(),2)
    aaaaaa = round(new_logits[0, top5[0, 0].item()].item() + new_logits[0, top5[0, -1].item()].item(),2)
    score = round(aaaaaa/sums,2) * 10
    print(top5[0, :])
    label_indexss = [asdf.item() for asdf in top5[0, :]]
    labels = [imagenet_labels[label_index] for label_index in label_indexss]
    
    att_mat = torch.stack(list(att_mat)).squeeze(1).to(device, torch.float)
    # Average the attention weights across all heads.
    att_mat = torch.mean(att_mat, dim=1).to(device, torch.float)
    # To account for residual connections, we add an identity matrix to the
    # attention matrix and re-normalize the weights.
    residual_att = torch.eye(att_mat.size(1)).to(device, torch.float)
    aug_att_mat = att_mat + residual_att
    aug_att_mat = aug_att_mat / aug_att_mat.sum(dim=-1).unsqueeze(-1)
    # Recursively multiply the weight matrices
    joint_attentions = torch.zeros(aug_att_mat.size())
    joint_attentions[0] = aug_att_mat[0]
    for n in range(1, aug_att_mat.size(0)):
        joint_attentions[n] = torch.matmul(aug_att_mat[n], joint_attentions[n-1])
    v = joint_attentions[-1]
    grid_size = int(np.sqrt(aug_att_mat.size(-1)))
    mask = v[0, 1:].reshape(grid_size, grid_size).detach().numpy()
    mask = cv2.resize(mask / mask.max(),image.size)[..., np.newaxis]
    result = (mask * image).astype("uint8")
    attention_image = Image.fromarray(result)
    attention_image.save(f"./ququ/apicode/Transformer/{global_user_name}.jpg")

    client = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=ACCESS_SECRET_KEY,
                      region_name=AWS_DEFAULT_REGION
                      )

    client.upload_file(f"./ququ/apicode/Transformer/{global_user_name}.jpg", BUCKET_NAME, f"upload/{asdf}_{global_user_name}_attentionmap.jpg")

    attention_url = f"https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/{asdf}_{global_user_name}_attentionmap.jpg"
    
    encoding_df = list(QuQuVectorEmbedding.objects.filter(col_season = season).exclude(col_styles__isnull=True).values()) #.order_by('-style_datetime')[0]["style_datetime"]
    df = pd.DataFrame(encoding_df)
    columnss = ["col_"+str(i) for i in range(128)] + ["row_name","col_styles","col_score"]
    df = df[columnss]
    list_name = [round(x,2) for x in t.tolist()[0]]
    uservectordf = pd.DataFrame(list_name, index=["col_"+str(i) for i in range(128)]).T
    similar_url = {}
    for i in set(list(df["col_styles"])):
        test = df[df['col_styles'] == i]
        cosine_results = cosine_similarity(uservectordf, test.drop(columns=['row_name','col_styles',"col_score"]))
        c_sim = cosine_results.argsort()[:,::-1]
        sim_index = c_sim[0][1:21]
        url_score_list = []
        for a,b in zip(test.iloc[sim_index]['row_name'], test.iloc[sim_index]['col_score']):
            url_score_dcit = {}
            url_score_dcit["url"] = "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/fw_2023/" + a.split(".png")[0] + ".jpg"
            if float(b) <= 10:
                b = 1
            elif float(b) <= 19:
                b = str(b)[1]
            elif float(b) >= 20:
                b = 10
            url_score_dcit["score"] = b
            url_score_list.append(url_score_dcit)
        similar_url[i] = url_score_list
    if float(score) <= 10:
        score = 1
    elif float(score) <= 19:
        score = str(score)[1]
    elif float(score) >= 20:
        score = 10
    os.remove(f"./ququ/apicode/Transformer/{global_user_name}.jpg")
    return score, labels, attention_url, similar_url
