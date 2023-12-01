import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np
from datetime import datetime
from ququ.models import *
import torch
# import time
# from multiprocessing import Process,Queue
# import ast
# import threading
# import os
# from queue import  
# from concurrent import futures
def K_result_dict(req_json):
    result_dict = {}
    for i in req_json['K-means']:
        for j in req_json['K-means'][i]:
            if req_json['K-means'][i][j]["status"]:
                true_image_list = []
                for jj in req_json['K-means'][i][j]["image"]:
                    if req_json['K-means'][i][j]["image"][jj]:
                        true_image_list.append(jj)
                result_dict['K-means' + i + j] = (true_image_list)
    return result_dict

def G_result_dict(req_json):
    result_dict = {}
    for i in req_json['K-means']:
        for j in req_json['K-means'][i]:
            if req_json['K-means'][i][j]["status"]:
                true_image_list = []
                for jj in req_json['K-means'][i][j]["image"]:
                    if req_json['K-means'][i][j]["image"][jj]:
                        true_image_list.append(jj)
                result_dict['K-means' + i + j] = (true_image_list)
    for i in req_json['GMM']:
        for j in req_json['GMM'][i]:
            if req_json['GMM'][i][j]["status"]:
                true_image_list = []
                for jj in req_json['GMM'][i][j]["image"]:
                    if req_json['GMM'][i][j]["image"][jj]:
                        true_image_list.append(jj)
                result_dict['GMM' + i + j] = (true_image_list)
    return result_dict

def make_corr(result_dict, encoding_df, subset_cat_attributes, global_user_name):

    df = pd.DataFrame(encoding_df).set_index("row_name")
    checklist = list(df.columns)
    for i in subset_cat_attributes :
        if i not in checklist:
            subset_cat_attributes.remove(i)
    df = df[subset_cat_attributes].astype(float)
    cluster_list = list(result_dict.keys())
    df_list = []
    for i in result_dict:
        image_dict = result_dict[i]
        df_dict = {}
        for j in cluster_list:
            df_dict[j] = 0
        df_dict[i] = 1
        df_test = df.loc[image_dict].sum(axis=0)
        for x,y in zip(df_test,list(df_test.index)):
            df_dict[y] = x
        df_list.append(df_dict)
    df_corr = pd.DataFrame(df_list).fillna(0)
    df_corr_corr = df_corr.corr().fillna(0).loc[cluster_list].drop(cluster_list, axis=1)
    ##########################################
    now = datetime.now()
    dddd = df_corr_corr.to_dict()
    save_user_data = UserLogs(
        user_name = global_user_name,
        correlation_datetime = now,
        user_correlation = dddd
    )
    save_user_data.save()
    ##########################################
    np_corr_corr = np.array(df_corr_corr)

    label = []
    score = []
    asdfgh = torch.mm(torch.Tensor(np.array(df)), torch.Tensor(np_corr_corr.T))
    # print(asdfgh)
    len_n = asdfgh.shape[0]
    for i in range(len_n):
        aaaaaa = torch.Tensor.numpy(asdfgh[i])
        tt = np.argmax(aaaaaa)
        # print(tt)
        a = list(df_corr_corr.index)[tt]
        # print(a)
        b = round(aaaaaa[tt],2)
        # print(str(b))
        label.append(a)
        score.append(str(b))

    df["new_clusterlabel"] = label
    df["score"] = score

    result = {}
    for i in cluster_list:
        result[i] = {}
        sorted_style = df[df["new_clusterlabel"] == i].sort_values(by = ["score"], ascending = False)

        image_names = list(sorted_style.index)

        result[i]["images"] = image_names[:30]

    return result, df
