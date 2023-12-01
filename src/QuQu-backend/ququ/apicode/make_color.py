import os
#from tqdm import tqdm
#from tqdm.notebook import tqdm
from PIL import Image
import numpy as np

import torch

import torch.nn.functional as F
import torchvision.transforms as transforms

from ququ.apicode.data.base_dataset import Normalize_image
from ququ.apicode.utils.saving_utils import load_checkpoint_mgpu

from ququ.apicode.networks import U2NET
import requests
import extcolors
import json
from collections import OrderedDict
import csv
import cv2
import pandas as pd

device = 'cuda'
checkpoint_path = './ququ/apicode/cloth_segm_u2net_latest.pth'

def get_palette(num_cls):
    """ Returns the color map for visualizing the segmentation mask.
    Args:
        num_cls: Number of classes
    Returns:
        The color map
    """
    n = num_cls
    palette = [0] * (n * 3)
    for j in range(0, n):
        lab = j
        palette[j * 3 + 0] = 0
        palette[j * 3 + 1] = 0
        palette[j * 3 + 2] = 0
        i = 0
        while lab:
            palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
            palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
            palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
            i += 1
            lab >>= 3
    return palette




def find_nearest(array_,value_):
    array_ = np.asarray(array_)
    idx = (np.abs(array_ - value_)).argmin()
    return array_[idx]

def color_label(list_a):
    color_df = pd.read_csv("./ququ/apicode/color_label.csv")
    RGB = list_a
    pixel = np.uint8([[RGB]])
    HSV = cv2.cvtColor(pixel, cv2.COLOR_RGB2HSV)
    H = HSV[0][0][0]
    S = HSV[0][0][1]
    V = HSV[0][0][2]

    # color label 
    # H
    if H <= 7 or H >= 173:
        H = 0
    else:
        array_H = np.array([15,30,45,60,75,90,105,120,135,150,165])
        value_H = H
        H = find_nearest(array_H,value_H)

    # S,V
    if S <= 30:
        if V <= 90:
            #black
            H,S,V = 0,0,0
        if V > 90 and V <=200:
            #gray
            H,S,V = 0,0,150
        if V > 200:
            #white
            H,S,V = 0,0,255
    else:
        if V <= 30:
            #black
            H,S,V = 0,0,0
        else:
            array_S = np.array([60,120,180,240])
            value_S = S
            S = find_nearest(array_S,value_S)
            array_V = np.array([60,120,180,240])
            value_V = V
            V = find_nearest(array_V,value_V)

    if [S,V] == [60,60] or [S,V] == [120,60]:
        H,S,V = 0,0,0
    elif [S,V] == [180,60] or [S,V] == [240,60]:
        S,V = 210,60
    elif [S,V] == [180,120] or [S,V] == [240,120]:
        S,V = 210,120
    elif [S,V] == [240,180] or [S,V] == [240,240]:
        S,V = 240,210

    df = color_df[color_df["HSV"] == "[{},{},{}]".format(H,S,V)]

    colorfilter = df.iloc[0][1]
    return colorfilter

def run_color(url_link):
    transforms_list = []
    transforms_list += [transforms.ToTensor()]
    transforms_list += [Normalize_image(0.5, 0.5)]
    transform_rgb = transforms.Compose(transforms_list)

    net = U2NET(in_ch=3, out_ch=4)
    net = load_checkpoint_mgpu(net, checkpoint_path)
    net = net.to(device)
    net = net.eval()

    palette = get_palette(4)

    url = url_link
    img = Image.open(requests.get(url, stream=True).raw)
    img_size = img.size
    re_img = img.resize((768, 768), Image.BICUBIC)
    image_tensor = transform_rgb(re_img)
    image_tensor = torch.unsqueeze(image_tensor, 0)
    output_tensor = net(image_tensor.to(device))
    output_tensor = F.log_softmax(output_tensor[0], dim=1)
    output_tensor = torch.max(output_tensor, dim=1, keepdim=True)[1]
    output_tensor = torch.squeeze(output_tensor, dim=0)
    output_tensor = torch.squeeze(output_tensor, dim=0)
    output_arr = output_tensor.cpu().numpy()
    output_img = Image.fromarray(output_arr.astype('uint8'), mode='L')
    output_img = output_img.resize(img_size, Image.BICUBIC)
    
    output_img.putpalette(palette)
    
    img_arr = np.array(output_img.resize((500,700)))
    mask = img_arr > 0
    image_array = np.array(img.resize((500,700)))
    PIL_image = Image.fromarray(image_array[mask].reshape(1,-1,3)).convert('RGB')
    colors, pixel_count = extcolors.extract_from_image(PIL_image)
    color_dict = {}
    for c in colors:
        color_dict["{},{},{}".format(c[0][0],c[0][1],c[0][2])] = round((c[1] / pixel_count) * 100, 2)
    print(color_dict)
    print(type(color_dict))

    only_main_color_dict = {}
    total_colors = []
    for x, RGBS in enumerate(list(color_dict.keys())):
        if x == 0 :
            # first main colot to dict
            list_a = list(map(int, RGBS.split(",")))
            colorfilter = color_label(list_a)
            total_colors.append(colorfilter)
        else:
            # second main color to dict if >= 10
            if float(color_dict[RGBS]) >= 10:
                list_a = list(map(int, RGBS.split(",")))
                colorfilter = color_label(list_a)
                total_colors.append(colorfilter)
    only_main_color_dict[url] = list(set(total_colors))

    return only_main_color_dict
