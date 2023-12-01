from ququ.models import *
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from .Transformer.script import *
from django.db import connection
def make_style_dict(global_user_name, label_result_t,color_result_t):

    cursor = connection.cursor()
    print("global_user_name", global_user_name)
    cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
    k = cursor.fetchall()[0][0]
    print("cursor.fetchall()", k)
    df = pd.read_sql_query(f'SELECT * FROM user_styles WHERE user_name="{global_user_name}" AND style_datetime = "{k}"',connection)

    print(df)
    ssd = list(eval(list(df["image_name_score"])[0]).keys())
    season = ssd[0].split('_')[1]
    if season == "F":
        season = "fw"
    else:
        season = "ss"

    temp_df = df[["new_clusterlabel", "style_name","original_name"]]

    style_dict = {}
    for a,b in zip(temp_df['new_clusterlabel'], temp_df['style_name']):
        style_dict[a] = b
    match_original_to_new = {}
    for a,b in zip(temp_df['original_name'], temp_df['style_name']):
        match_original_to_new[a] = b
    match_new_to_original = {}
    for a,b in zip(temp_df['style_name'], temp_df['original_name']):
        match_new_to_original[a] = b
    ##correalation df 
    temp_dict = UserLogs.objects.filter(user_name = global_user_name).exclude(correlation_datetime__isnull=True).values().order_by('-correlation_datetime')[0]["user_correlation"]
    df_corr_corr = pd.DataFrame.from_dict(eval(temp_dict))
    checklist = list(df_corr_corr.columns)
    ## attribute detection result to dataframe 
    col_list = []
    for i in label_result_t:
        a = i["category"]
        if len(i["attributes"]) > 0 :
            for b in i["attributes"]:
                col_list.append("col"+"_"+f"{a}"+"_"+f"{b}")
        else:
            col_list.append("col"+"_"+f"{a}"+"_"+"field")
    col_list = col_list + ["col_"+abc for abc in list(color_result_t.values())[0]]
    detec_df = pd.DataFrame(index = range(0,1), columns=checklist)
    for i in col_list:
        if i in checklist:
            detec_df[i] = 1
    detec_df = detec_df.fillna(0)
    detec_np = np.array(detec_df)
    return style_dict, col_list, detec_np, detec_df, df_corr_corr, match_original_to_new, match_new_to_original, df, season

def normalization(x):
    min_value = min(x)
    max_value = max(x) 

    return list(map(lambda x: (x-min_value)/(max_value-min_value), x))

def improve(label_result_t, global_user_name, color_result_t, url, bgremove_url,ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME):
    # transformer output
    style_dict, col_list, detec_np, detec_df, df_corr_corr, match_original_to_new, match_new_to_original, df, season = make_style_dict(global_user_name,label_result_t,color_result_t)
    score, labels, attention_url, similar_url = style_classification(bgremove_url, season, global_user_name,ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME)

    encoding_df2 = list(QuquCatAttrEncoding.objects.filter( col_season=season).values()) #col_year=year,
    encoding_df2 = pd.DataFrame(encoding_df2).drop(columns='id').set_index("row_name")
    dict_for_df = {}
    for k,b in zip(df["image_name_score"], df["style_name"]):
        ttttt = dict(json.loads(k))
        for i in ttttt:
            dict_for_df[i] = [b,ttttt[i]]
    style_df = pd.DataFrame.from_dict(data=dict_for_df, orient='index') #.reset_index(drop= False)
    style_df = style_df.rename(columns={0:"col_styles",1:"score"})
    style_df_vector = pd.concat([style_df,encoding_df2], axis=1)
    detec_df["col_styles"] = "None"
    df_cate_attr = pd.concat([detec_df,style_df_vector], join ="inner")
    df_cate_attr = df_cate_attr.reset_index()

    result = {}
    result["target_style"] = {}
    df_corr_corr = df_corr_corr.rename(style_dict, axis=0)

    #score sum
    scores_sum_list = []
    for styles in df_corr_corr.index:
        style_np = np.array(pd.DataFrame(df_corr_corr.loc[styles]).T)
        aaa = detec_np * style_np
        scores_sum_list.append(aaa.sum())
    norm_scores_sum_list = normalization(scores_sum_list)
    scores_sum = sum(norm_scores_sum_list)

    # calculate target style
    for styles, scores in zip(df_corr_corr.index, norm_scores_sum_list):
        result["target_style"][styles] = {}
        print(styles)
        #target style improvement attribute
        test_df = pd.DataFrame(df_corr_corr.loc[styles])
        tttt = list(test_df[test_df[styles] >= 0][styles].sort_values(ascending=False).index)
        for b in tttt:
            if b in col_list:
                tttt.remove(b)
        
        #target style improvement attribute number to  text and input to result
        result["target_style"][styles]["improvement"] = []
        for i in tttt:
            t_dict = {}
            a = i.split("_")[1]
            b = i.split("_")[2]
            if a.isnumeric():
                c = list(QuquCategory.objects.filter(id = a).values())[0]["name"]
                if b == "field":
                    d = "*"
                else:
                    d = list(QuquAttributes.objects.filter(id = b).values())[0]["name"]
            else:
                c = a
                d = b
            t_dict["attribute"] = c + "_" + d
            t_dict["status"] = "false"
            result["target_style"][styles]["improvement"].append(t_dict)

        improvement_score_ = round(round(scores/scores_sum,2) * 10, 2)
        result["target_style"][styles]["improvement_score"] = improvement_score_
        
        test = df_cate_attr[df_cate_attr['col_styles'] == styles]
        test_one = df_cate_attr[df_cate_attr["index"] == 0]
        cosine_results = cosine_similarity(test_one.drop(columns=['index','col_styles']), test.drop(columns=['index','col_styles']))
        c_sim = cosine_results.argsort()[:,::-1]
        sim_index = c_sim[0][1:50]
        output = test.iloc[sim_index]["index"]
        result["target_style"][styles]["improvement_images"] = []
        for kk in output:
            ddddd = {}
            ssss = style_df.loc[kk][1]
            ddddd["url"] = "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/fw_2023/" + kk
            ddddd["score"] = ssss
            
            result["target_style"][styles]["improvement_images"].append(ddddd)

        match_index = []
        for matchone in match_original_to_new:

            match_index.append(int(labels.index(matchone)))
        match_index.sort()
        sorted_index = match_index[0]
        new_label = labels[sorted_index]
        result["target_style"][styles]["style"] = match_original_to_new[new_label]

        result["target_style"][styles]["score"] = score
        result["target_style"][styles]["attention_map"] = attention_url
        result["target_style"][styles]["attention_map_images"] = similar_url[match_new_to_original[styles]]

    result["labeling_result"] = col_list
    return result



def selectimprove(global_user_name, col_list, selected_attribute, selected_style):

    cursor = connection.cursor()
    cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
    k = cursor.fetchall()[0][0]
    df = pd.read_sql_query(f'SELECT * FROM user_styles WHERE user_name="{global_user_name}" AND style_datetime = "{k}"',connection)

    style_dict = {}
    for a,b in zip(df['new_clusterlabel'], df['style_name']):
        style_dict[a] = b
    dict_for_df = {}
    for k,b in zip(df["image_name_score"], df["style_name"]):
        ttttt = dict(json.loads(k))
        for i in ttttt:
            dict_for_df[i] = [b,ttttt[i]]
    style_df = pd.DataFrame.from_dict(data=dict_for_df, orient='index') #.reset_index(drop= False)
    ssd = list(eval(df["image_name_score"][0]).keys())

    season = ssd[0].split('_')[1]
    if season == "F":
        season = "fw"
    else:
        season = "ss"
    year = "20" + ssd[0].split('_')[2]
    temp_dict = UserLogs.objects.filter(user_name = global_user_name).exclude(correlation_datetime__isnull=True).values().order_by('-correlation_datetime')[0]["user_correlation"]
    df_corr_corr = pd.DataFrame.from_dict(eval(temp_dict))
    checklist = list(df_corr_corr.columns)

    selected_list  = []
    for i in selected_attribute:
        print(i)
        a = i.split("_")[0]
        b = i.split("_")[1]
        if a in ["vivid","basic","dark","grayish","light"]:
            c = a
            d = b
        else:
            c = list(QuquCategory.objects.filter(name = a).values())[0]["id"]
            if b == "*":
                d = "field"
            else:
                d = list(QuquAttributes.objects.filter(name = b).values())[0]["id"]
        selected_list.append("col_" + str(c) + "_"+str(d))
    col_list = col_list + selected_list
    print(col_list)

    detec_df = pd.DataFrame(index = range(0,1), columns=checklist)
    for i in col_list:
        if i in checklist:
            detec_df[i] = 1
    detec_df = detec_df.fillna(0)
    styles = selected_style.replace("\"","")

        
    style_df = style_df.rename(columns={0:"col_styles",1:"score"})
    
    encoding_df2 = list(QuquCatAttrEncoding.objects.filter( col_season=season).values()) #col_year=year,
    encoding_df2 = pd.DataFrame(encoding_df2).drop(columns='id').set_index("row_name")
    style_df_vector = pd.concat([style_df,encoding_df2], axis=1)
    
    detec_df["col_styles"] = "None"
    df_cate_attr = pd.concat([detec_df,style_df_vector], join ="inner")
    df_cate_attr = df_cate_attr.reset_index()
    test = df_cate_attr[df_cate_attr['col_styles'] == styles]
    test_one = df_cate_attr[df_cate_attr["index"] == 0]
    cosine_results = cosine_similarity(test_one.drop(columns=['index','col_styles']), test.drop(columns=['index','col_styles']))
    c_sim = cosine_results.argsort()[:,::-1]
    sim_index = c_sim[0][1:50]
    output = test.iloc[sim_index]['index']
    result = {}
    result["improvement_images"] = []

    for i in output:
        ddddd = {}
        ssss = style_df.loc[i][1]
        ddddd["url"] = "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/fw_2023/" + i
        ddddd["score"] = ssss
        result["improvement_images"].append(ddddd) 
    return result

