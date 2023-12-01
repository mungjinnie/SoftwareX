from mmdet.apis import (async_inference_detector, inference_detector,init_detector) #show_result_pyplot)
import os 
import random
import cvlib as cv
import cv2
import numpy as np
import uuid
import shutil
import pandas as pd
import json
import torch
#from labeling import labeling
from tqdm import tqdm
import urllib.request
from PIL import Image
import requests


with open('./ququ/apicode/FashionFormer/attr_idx.json', 'r') as f:
    with_attr_idx = json.load(f)


def list_sort(attr_list):
    return sorted(list(set(attr_list)))
                  

def get_top1_with_attr(with_attr_inds, attr):
    for i in with_attr_inds:
        match_dict = {k: attr[k] for k in i}
        sort_match_dict = sorted(match_dict.items(), key = lambda item: item[1], reverse = True)
        top_1_with_attr = sort_match_dict[:1][0][0]  
    return top_1_with_attr

def get_label_result(detect_result):
    global with_attr_idx
    for k in range(0, len(detect_result)):
        try:
            detect_result[k]['score'] = [i[0][-1] for i in detect_result[k]['category_score']]
        except:
            pass
    
    image = []
    for x in range(0, len(detect_result)):
        getList = [i for i,v in enumerate(detect_result[x]['score']) if v >= 0.8]
        cate =  [detect_result[x]['category_id'][i] for i in getList]
        t = [detect_result[x]['attribute'][i][0] for i in getList]
        with_attribute = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 28, 29, 30, 31, 32, 33]
        for idx, c in enumerate(cate):
            temp = {}
            temp['image'] = detect_result[x]['name']
            temp['category'] = int(c)
            if c in with_attribute:
                attr = t[idx]
                sort_attr_inds = attr.argsort()[::-1]
                sort_attr_score = attr[sort_attr_inds] > 0.5
                num_over_thr = list(sort_attr_score).count(True)
                attr_list = list(sort_attr_inds[:num_over_thr])
                attr_list = list([int(x) for x in attr_list])
                if c == 0: # shirt
                    shirt = with_attr_idx[1].values()
                    top_1_with_attr = get_top1_with_attr(shirt, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
                elif c == 1: # top
                    top = with_attr_idx[0].values()
                    top_1_with_attr = get_top1_with_attr(top, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
                elif c == 4: # jacket
                    jacket = with_attr_idx[2].values()
                    top_1_with_attr = get_top1_with_attr(jacket, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
                elif c == 6: # pants
                    pants = with_attr_idx[3].values()
                    top_1_with_attr = get_top1_with_attr(pants, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 7: #  shorts
                    shorts = with_attr_idx[4].values()
                    top_1_with_attr = get_top1_with_attr(shorts, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 8: # skirt
                    skirt = with_attr_idx[5].values()
                    top_1_with_attr = get_top1_with_attr(skirt, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
                elif c == 9: # coat
                    coat = with_attr_idx[6].values()
                    top_1_with_attr = get_top1_with_attr(coat, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 10: # dress
                    dress = with_attr_idx[7].values()
                    top_1_with_attr = get_top1_with_attr(dress, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 28: # collar
                    collar = with_attr_idx[14].values()
                    top_1_with_attr = get_top1_with_attr(collar, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 29: # lapel
                    lapel = with_attr_idx[13].values()
                    top_1_with_attr = get_top1_with_attr(lapel, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
                elif c == 31: # sleeve
                    sleeve = with_attr_idx[11].values()
                    top_1_with_attr = get_top1_with_attr(sleeve, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 32: # pocket
                    pocket = with_attr_idx[12].values()
                    top_1_with_attr = get_top1_with_attr(pocket, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
    
                elif c == 33: # neckline
                    neckline = with_attr_idx[8].values()
                    top_1_with_attr = get_top1_with_attr(neckline, attr)
                    attr_list.append(top_1_with_attr)
                    attr_list = list_sort(attr_list)
                if 270 in attr_list:
                    attr_list.remove(270)
                if 269 in attr_list:
                    attr_list.remove(269)
                if 248 in attr_list:
                    attr_list.remove(248)
                if 115 in attr_list:
                    attr_list.remove(115)
                temp['attributes'] = attr_list
            else:
                temp['attributes'] = []
            image.append(temp)
    return image

def start_model(url, global_user_name):
    image_name = global_user_name
    path = "./ququ/apicode/FashionFormer/image_folder/"
    img = Image.open(requests.get(url.replace("\"", ""), stream = True).raw)
    try:
        img.save( "{}{}.jpg".format(path, image_name))
    except:
        img = img.convert('RGB')
        img.save( "{}{}.jpg".format(path, image_name))
    config_file = './ququ/apicode/FashionFormer/configs/attribute_mask_rcnn/attribute_mask_rcnn_swin_b_3x.py'
    checkpoint_file = './ququ/apicode/FashionFormer/work_dirs/attribute_mask_rcnn_swin_b_3x_/fashionformer_swin_b_3x.pth'
    model = init_detector(config_file, checkpoint_file, device='cuda:0')
    detect_result = []
    bbox_result, segm_result, attr_result = inference_detector(model,"{}{}.jpg".format(path, image_name))
    result_dict = {}
    result_dict['name'] = image_name
    result_dict['category_id'] = [i for i,v in enumerate(bbox_result) if len(v) != 0]
    result_dict['category_score'] = [v for i,v in enumerate(bbox_result) if len(v) != 0]
    result_dict['attribute'] = [v for i,v in enumerate(attr_result) if len(v) != 0]
    detect_result.append(result_dict)
    images = get_label_result(detect_result)
    return images