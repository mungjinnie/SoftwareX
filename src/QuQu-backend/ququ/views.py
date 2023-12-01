import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","ququ_backend.settings")
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .apicode.cat_attr import *
from .apicode.cluster import *
# from .apicode.image_attr import *
from .apicode.naming import *
from .apicode.improvement import *
from .apicode.make_color import *
from .apicode.HumanGAN.alignment import *
from .apicode.HumanGAN.interpolation import *
# from .apicode.HumanGAN.interpolation_vogue import *
from .apicode.HumanGAN.edit_run import *
from .apicode.HumanGAN.style_mixing import *
import urllib.request
from ququ.models import *
from django.http import JsonResponse
import re
import json
import boto3
import requests
import shutil
from django.core import serializers
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.db import connection
import ast
from datetime import datetime
from django.http import QueryDict
import pandas as pd
import random
from django.conf import settings

###INPUT USER INFO
global_user_name = ""

ACCESS_KEY_ID = getattr(settings, 'ACCESS_KEY_ID', None)
ACCESS_SECRET_KEY = getattr(settings, 'ACCESS_SECRET_KEY', None)
AWS_DEFAULT_REGION = getattr(settings, 'AWS_DEFAULT_REGION', None)
BUCKET_NAME = getattr(settings, 'BUCKET_NAME', None)


# Create your views here.
@csrf_exempt
def index(request):
    print(request.POST)
    return HttpResponse('Hello')

def read(request, id):
    return HttpResponse('Welcome:)' + id)

@csrf_exempt
def username(request):
    user_name = request.POST['user_name'].lstrip('"').rstrip('"')
    global global_user_name
    print(user_name, global_user_name)
    if global_user_name == user_name:
        save_user_data = UserLogs(
            user_name = global_user_name
        )
        save_user_data.save()
    elif global_user_name != user_name: 
        raise KeyError

    return HttpResponse()

@csrf_exempt
def getCatandAttr(request, ys):    
    year = re.findall('\d+', ys)[0]
    season = re.findall('[A-Z]+', ys)[0].lower()
    result = make_result(year, season)
    print(year, season)
    return JsonResponse(result, safe=False)
    

@csrf_exempt
def getImageAttr(request):

    req = request.POST.dict()
    print(req)
    if 'url' in list(req.keys()):
        url = req["url"]
        global global_user_name
        label_result_t = run_detection(url,global_user_name)
        attribute_list = []
        for i in label_result_t:
            a = i["category"]
            for j in i["attributes"]:
                attribute_list.append(str(a) + "_" + str(j))
        
        brand_list = "|".join(attribute_list)
        print(brand_list)

    elif 'brand_name' in list(req.keys()):
        brand = req["brand_name"]
        year = "20" + req["ys"][:2]
        season = req["ys"][2:].lower()
        brand_list = list(QuquBrandAtt.objects.filter(year=year, season=season, brand = brand).values())[0]['attribute']
    result =  make_result2(brand_list)
    print(result)
    return JsonResponse(result, safe=False)



@csrf_exempt
def getClustering(request):
    # get cat_attr from previous page
    req_json = json.loads(request.POST['category'])
    color_json = json.loads(request.POST['color'])
    method = json.loads(request.POST['method'])
    ys = json.loads(request.POST['ys'])
    global global_user_name
##################################
    clicked = eval(request.POST['log'])['clicked']
    types = "clicked"
    sss = eval(request.POST['log'])['season']
    now = datetime.now()
    print(clicked,sss)
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = clicked,
        season = sss,
        date_time = now,
        types = types
    )
    save_user_data.save()    
###############################
    year = re.findall('\d+', ys)[0]
    full_year = "20" + year
    season = re.findall('[A-Z]+', ys)[0].lower()

    selected_item = []

    for x in req_json:
        for xx in req_json[x]:
            if req_json[x][xx]['status']: 
                if str(req_json[x][xx]['category']) in ["13","14","15","16","17","18","19","20","21","22","24","25","26","27","30","34","35","36","37","38","39","40","41","42","43","44","45"]:
                    selected_item.append(str(req_json[x][xx]['category']) + '_' + 'field')
                else:
                    selected_item.append(str(req_json[x][xx]['category']) + '_' + str(req_json[x][xx]['attribute']))
    for x in color_json:
        for xx in color_json[x]:
            if color_json[x][xx]['status']: 
                selected_item.append(str(color_json[x][xx]['category']) + '_' + str(color_json[x][xx]['attribute']))
    selected_item = selected_item + ['basic_tone', 'dark_tone', 'grayish_tone', 'light_tone', 'vivid_tone']
    #get clustering result
    #method = K-means, then k-means=15
    if method == 'K-means':
        attributepage = 0
    #method = GMM, then k-means and GMM both        
    if method == "GMM":
        attributepage = 1
    result = make_G_dict(selected_item,year,season)
#    print(result)
    now = datetime.now()
    
    #when finished selecting attribute, selected feature
    save_user_data = UserLogs(
        user_name = global_user_name,
        attribute_datetime = now,
        selected_item = selected_item,
        attributepage = attributepage
    )
    save_user_data.save()
    #print(result['K-means']["clusters"]['k15'])
    print(result)
    return JsonResponse(result, safe=False)

@csrf_exempt
def getStyle(request):
    global global_user_name
    req_json = request.POST
    ys = json.loads(req_json['ys'])
    year = re.findall('\d+', ys)[0]
    season = re.findall('[A-Z]+', ys)[0].lower()
    clusterpage = json.loads(req_json['free'])
    now = datetime.now()
    print(req_json)
    # save database
    save_user_data = UserLogs(
        user_name = global_user_name,
        cluster_datetime = now,
        clusterpage = clusterpage
    )
    save_user_data.save()
    clicked = eval(req_json['log'])['clicked']
    types = "clicked"
    # sss = json.loads(request.POST['log']['season'])
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = clicked,
        season = season,
        date_time = now,
        types = types
    )
    save_user_data.save()    
    req_json = json.loads(req_json['methods'])

    result_dict = G_result_dict(req_json)
    encoding_df = list(QuquCatAttrEncoding.objects.filter(col_year=year, col_season=season).values())
    selected_item = UserLogs.objects.filter(user_name = global_user_name).exclude(
        attribute_datetime__isnull=True).values().order_by('-attribute_datetime')[0]["selected_item"]
    subset_cat_attributes = list(map(lambda x:'col_'+x, ast.literal_eval(selected_item))) #+ ast.literal_eval(selected_image)
    result, df = make_corr(result_dict, encoding_df, subset_cat_attributes, global_user_name)
    new_clusterlabel = df.new_clusterlabel
    db_insert = []
    for i in set(new_clusterlabel):
        sorted_style = df[df["new_clusterlabel"] == i].sort_values(by = ["score"], ascending = False)
        image_names = list(sorted_style.index)
        image_scores = list(sorted_style.score)
        db_dict = {}
        for x,y in zip(image_names, image_scores):
            db_dict[x] = y
        db_insert.append((global_user_name, json.dumps(db_dict), i, now))
    db_insert = tuple(db_insert)
    # save style naming to DB
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO user_styles(user_name, image_name_score, new_clusterlabel, style_datetime)VALUES(?,?,?,?)", db_insert)
    connection.commit()
    #############################################
    # change_key = {}
    # for i,j in enumerate(before_result.keys()):
    #     change_key[j] = "userstyle" + str(i+ 1)
    # result = dict((change_key[key], value) for (key, value) in before_result.items())
    #############################################
    print(result)
    return JsonResponse(result, safe=False)

@csrf_exempt
def saveStyle(request, ys):
    global global_user_name
    req_json = json.loads(list(request.POST.dict().keys())[0])
    print(req_json)
##################################
    now = datetime.now()
    clicked = req_json['log']['clicked']
    types = "clicked"
    try:
        sss = req_json['log']['season']
    except:
        sss = "TEST"
    print(clicked,sss)
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = clicked,
        season = sss,
        date_time = now,
        types = types
    )
    save_user_data.save()    
###############################
    check_ = list(req_json.keys())[0]
    keylist = list(req_json.keys())[:-1]
    
    if "K-means" in check_ or "GMM" in check_:
        if ys == "2023SS":
            style_name_dict = {"K-meansk15dark_punk":"dark_punk","K-meansk15elegance":"elegance","K-meansk15oversized_grunge":"oversized_grunge","K-meansk15casual_simple":"casual_simple","K-meansk15sexy_chic":"sexy_chic","K-meansk15street_punk":"street_punk","K-meansk15pure_feminine":"pure_feminine","K-meansk15formal":"formal","K-meansk15street_casual":"street_casual","K-meansk15feminine_grunge":"feminine_grunge","K-meansk15hip_hop":"hip_hop","K-meansk15vivid_punk":"vivid_punk","K-meansk15chic_elegance":"chic_elegance","K-meansk15sexy_feminine":"sexy_feminine","K-meansk15bohemian_feminine":"bohemian_feminine"}
            for style_namess in style_name_dict:
                cursor = connection.cursor()
                cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
                k = cursor.fetchall()[0][0]
                original_name = style_name_dict[style_namess]
                cursor = connection.cursor()
                cursor.execute("UPDATE user_styles SET style_name = '%s' WHERE user_name= '%s' and new_clusterlabel= '%s' and style_datetime = '%s'"%(original_name,global_user_name,style_namess,k))
                connection.commit()
                cursor = connection.cursor()
                cursor.execute("UPDATE user_styles SET original_name = '%s' WHERE user_name= '%s' and new_clusterlabel= '%s' and style_datetime = '%s'"%(original_name,global_user_name,style_namess,k))
                connection.commit()
        elif ys == "2023FW":
            style_name_dict = {"K-meansk15bohemian_elegance":"bohemian_elegance","K-meansk15chic_formal":"chic_formal","K-meansk15tomboy":"tomboy","K-meansk15sexy_feminine":"sexy_feminine","K-meansk15dark_romance":"dark_romance","K-meansk15formal":"formal","K-meansk15rock_chic":"rock_chic","K-meansk15hip_hop":"hip_hop","K-meansk15vintage_street":"vintage_street","K-meansk15sexy_street":"sexy_street","K-meansk15feminine_casual":"feminine_casual","K-meansk15elegance":"elegance","K-meansk15cozy_casual":"cozy_casual","K-meansk15chic_grunge":"chic_grunge","K-meansk15basic_casual":"basic_casual"}
            for style_namess in style_name_dict:
                cursor = connection.cursor()
                cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
                k = cursor.fetchall()[0][0]
                original_name = style_name_dict[style_namess]
                cursor = connection.cursor()
                cursor.execute("UPDATE user_styles SET style_name = '%s' WHERE user_name= '%s' and new_clusterlabel= '%s' and style_datetime = '%s'"%(original_name,global_user_name,style_namess,k))
                connection.commit()
                cursor = connection.cursor()
                cursor.execute("UPDATE user_styles SET original_name = '%s' WHERE user_name= '%s' and new_clusterlabel= '%s' and style_datetime = '%s'"%(original_name,global_user_name,style_namess,k))
                connection.commit()
    else:
        # get most recently saved style by the user
        i = list(req_json.keys())[0]
        j = req_json[i]["old_name"]
        cursor = connection.cursor()
        cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
        print(global_user_name)
        k = cursor.fetchall()[0][0]

        # get most recently saved style by the user
        cursor = connection.cursor()
        image_df_user = pd.read_sql_query(f'SELECT * FROM user_styles WHERE user_name="{global_user_name}" AND style_datetime = "{k}"',connection)
        findout_newname_user = {}
        dict_for_db = {}
        for image_name_score, new_clusterlabel in zip(image_df_user["image_name_score"],  image_df_user['new_clusterlabel']):
            for keyss in keylist:
                if req_json[keyss]["old_name"] == new_clusterlabel:
                        style_name = keyss
                        print(style_name)
            findout_newname_user[style_name] = list(eval(image_name_score).keys())
            dict_for_db[style_name] = {}
            dict_for_db[style_name]["new_clusterlabel"] = new_clusterlabel
        # get the style saved in DB
        cursor = connection.cursor()
        if ys == "2023SS":
            season = "ss"
        elif ys == "2023FW":
            season = "fw"
        image_df_db = pd.DataFrame(QuQuPredefinedStyles.objects.filter(season = season).values())
        findout_newname_db = {}
        for image_name_score, style_name in zip(image_df_db["image_name_score"], image_df_db["original_name"]):
            findout_newname_db[style_name] = list(eval(image_name_score).keys())

        for ii in findout_newname_user:
            lists = findout_newname_user[ii]
            counts = 0
            # check the the style saved by user and every style saved in db
            for iiii in findout_newname_db:
                aa = len(set(findout_newname_db[iiii]).intersection(set(lists)))
                if aa >= counts:
                    counts = aa
                    foundout = iiii

            # matched style saves in dict
            dict_for_db[ii]["original_name"] = foundout

            #save to DB
        for iiiii in dict_for_db:
            new_clusterlabel = dict_for_db[iiiii]["new_clusterlabel"]
            original_name = dict_for_db[iiiii]["original_name"]
            cursor = connection.cursor()
            cursor.execute("UPDATE user_styles SET style_name = '%s' WHERE user_name= '%s' and new_clusterlabel= '%s' and style_datetime = '%s'"%(iiiii,global_user_name,new_clusterlabel,k))
            connection.commit()
            cursor = connection.cursor()
            cursor.execute("UPDATE user_styles SET original_name = '%s' WHERE user_name= '%s' and new_clusterlabel= '%s' and style_datetime = '%s'"%(original_name,global_user_name,new_clusterlabel,k))
            connection.commit()
    print("saved!")
    # print("saveStyle", result)
    return JsonResponse(None, safe=False)

@csrf_exempt
def viewStyle(request):
    print(request)
    global global_user_name
    cursor = connection.cursor()
    cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
    k = cursor.fetchall()[0][0]
    df = pd.read_sql_query(f'SELECT * FROM user_styles WHERE user_name="{global_user_name}" AND style_datetime = "{k}"',connection)
    result = {}
    result["target_design"] = list(df.style_name)
    print(result)
    return JsonResponse(result, safe=False)

@csrf_exempt
def improvement(request):
    #attribute detection run
    print(request)
    req = request.POST.dict()
    url = req["url"]
    global global_user_name
    global global_user_name
    global ACCESS_KEY_ID
    global ACCESS_SECRET_KEY
    global AWS_DEFAULT_REGION
    global BUCKET_NAME

    url = url.replace("\"", "")
    # label_result_t = run_detection(url.replace("\"", ""),global_user_name)
    category_1 = [16,281,135,141,14,147,146,254,116,137,114,2,11,12,136,278,0,13,9,266,145,8,142,10,273]
    category_8 = [229,71,72,75,127,260,123,152,150,258,238,235,281,141,268,230,121,64,257,74,149,69,129,254,70,155,275,153,120,67,133,262,77,151,278,251,68,154,128,62,65,148,142,118]
    category1 = random.sample(category_1,4)
    category8 = random.sample(category_8,4)
    label_result_t = [{'image': global_user_name, 'category': 1, 'attributes': category1}
                      , {'image': global_user_name, 'category': 8, 'attributes': category8}]
    color_result_t = run_color(url)
    input_path = "./ququ/apicode/HumanGAN/img/test/"
    output_path = "./ququ/apicode/HumanGAN/aligned_image/"
    urllib.request.urlretrieve(url, "{}{}.jpg".format(input_path, global_user_name))
    bgremove_url = alignment_run(output_path, input_path, global_user_name, ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME)
    bgremove_url = bgremove_url[global_user_name]
    result = improve(label_result_t, global_user_name, color_result_t, url, bgremove_url,ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME)
    result = json.dumps(result)
    os.remove("{}{}.jpg".format(input_path, global_user_name))
    return JsonResponse(result, safe=False)
    
@csrf_exempt
def slectimprovement(request):
    req = request.POST.dict()
    print(req)
    selected_attribute, image_url, selected_style, col_list = ast.literal_eval(req["attribute"]), req["image"], req["style"], ast.literal_eval(req["labeling_result"])
    global global_user_name
    print("selected_attribute",selected_attribute)
    print("selected_style",col_list)
    result = selectimprove(global_user_name, col_list, selected_attribute, selected_style)
    return JsonResponse(result, safe=False)

@csrf_exempt
def randomgeneration(request):
    req = request.POST.dict()
    print(req)
    global global_user_name
    diversity, quality, style = req["diversity"], req["quality"], req["style"].replace("\"","")
##################################
    now = datetime.now()
    clicked = eval(req['log'])['clicked']
    types = "clicked"
    try:
        sss = eval(req['log'])['season']
    except:
        sss = "TEST"
    print("here",clicked, sss)
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = clicked,
        season = sss,
        date_time = now,
        types = types
    )
    save_user_data.save()    
###############################

    cursor = connection.cursor()
    cursor.execute(f'SELECT style_datetime FROM user_styles WHERE user_name="{global_user_name}" ORDER BY style_datetime DESC LIMIT 1')
    k = cursor.fetchall()[0][0]            

    df = pd.read_sql_query(f'SELECT * FROM user_styles WHERE user_name="{global_user_name}" AND style_datetime = "{k}"',connection)
    match_dict = {}
    for a,b in zip(df.style_name, df.original_name):
        match_dict[a] = b
    season = list(eval(list(df.image_name_score)[0]).keys())[0].split("_")[1]
    if season =='F':
        season = "fw23"
    elif season == 'S':
        season = "ss23"
    option_type = season + "|" + str(int(diversity)-1) +"|" + str(int(quality)-1)
    G_df = pd.DataFrame(list(QuquGeneration.objects.filter(option_type = option_type).values()))
    style_list = eval(G_df.style_list[0])[match_dict[style]]

    randomlist = random.sample(style_list, 12)
    result = {}
    result["info"] = []
    for kkkk, i in enumerate(randomlist):
        ddict= {}
        ddict["diversity"], ddict["quality"], ddict["style"] = diversity, quality, style
        ddict["url"] = "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/GAN/" +option_type+"|"+ i
        ddict["number"] = kkkk
        result["info"].append(ddict)
    print(result)
    return JsonResponse(result, safe=False)

@csrf_exempt
def GANmodels(request):
    global ACCESS_KEY_ID
    global ACCESS_SECRET_KEY
    global AWS_DEFAULT_REGION
    global BUCKET_NAME
    global global_user_name

    req = request.POST.dict()
    method = req['method']
    result = {}
    req["info"] = eval(req["info"])
##################################
    now = datetime.now()
    clicked = eval(req['log'])['clicked']
    types = "clicked"
    try:
        sss = eval(req['log'])['season']
    except:
        sss = "TEST"
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = clicked,
        season = sss,
        date_time = now,
        types = types
    )
    save_user_data.save()    
###############################    
    if method == "attributeedit":
        if req["info"][0]['style'] != "none":
            real = False
            reuse_pti = False
            bgremove_url= req["info"][0]['url']
            url1 = req["info"][0]['url']
            seeds = [int(url1.split("|")[-1].replace(".png",""))]
            image_names = url1.split("/")[-1]
        elif req["info"][0]['style'] == "none":
            raise KeyError

        
        network_pkl1 = ["quality0.pkl","quality1.pkl","quality2.pkl"][int(req["info"][0]['quality'])-1]
        trunc1 = [0.5,1.0,1.5][int(req["info"][0]['diversity'])-1]
        staa = req["length"].replace("\"","")
        print("staa",staa)
        attr_name = req["location"].replace("\"","") + "_length"
        print(attr_name)
        edit_url = edit_run(real, bgremove_url,global_user_name, seeds, trunc1,staa, attr_name, network_pkl1, reuse_pti, image_names,ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME)

        result["url"] = edit_url

    elif method == "interpolation":
        if req["info"][0]['style'] != "none":
            network_pkl1 = ["quality0.pkl","quality1.pkl","quality2.pkl"][int(req["info"][0]['quality'])-1]
            trunc1 = [0.5,1.0,1.5][int(req["info"][0]['diversity'])-1]
            network_pkl2 = ["quality0.pkl","quality1.pkl","quality2.pkl"][int(req["info"][1]['quality'])-1]
            trunc2 = [0.5,1.0,1.5][int(req["info"][1]['diversity'])-1]
            url1 = req["info"][0]['url']
            url2 = req["info"][1]['url']
            seed1 = int(url1.split("|")[-1].replace(".png",""))
            seed2 = int(url2.split("|")[-1].replace(".png",""))
            interpolation_url = interpolation_random(network_pkl1, seed1, trunc1, network_pkl2, seed2, trunc2,global_user_name,ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME)        
        elif req["info"][0]['style'] == "none":
            raise KeyError

        result["url"] = interpolation_url
        print(interpolation_url)

    elif method =="stylemixing":
        if req["info"][0]['style'] != "none":
            real = False
            url1 = req["info"][0]['url']
            url2 = req["info"][1]['url']
            seed1 = int(url1.split("|")[-1].replace(".png",""))
            seed2 = int(url2.split("|")[-1].replace(".png",""))
            image_names1 = url1.split("/")[-1]
            image_names2 = url2.split("/")[-1]
            reuse_pti = False
        elif req["info"][0]['style'] == "none":
            raise KeyError

   
        truncation_psi = [0.5,1.0,1.5][int(req["info"][0]['diversity'])-1]
        network_pkl = ["quality0.pkl","quality1.pkl","quality2.pkl"][int(req["info"][0]['quality'])-1]
        col_styles = [i for i in range(int(req['degree']) * 3)]
        print(col_styles)
        mixing_url = generate_style_mix(seed1,seed2, url1, url2, real, network_pkl, col_styles, truncation_psi,global_user_name,reuse_pti,image_names1,image_names2,ACCESS_KEY_ID, ACCESS_SECRET_KEY, AWS_DEFAULT_REGION, BUCKET_NAME)
        result["url"] = mixing_url
        print(mixing_url)
    return JsonResponse(result, safe=False)

@csrf_exempt
def saveToggle(request):
    global global_user_name
    req = request.POST.dict()
    print("here", req)
    toggle = eval(req["log"])["toggle"]
    season = eval(req["log"])["season"]
    now = datetime.now()
    types = "toggle"
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = toggle,
        season = season,
        date_time = now,
        types = types
    )
    save_user_data.save()
    return JsonResponse(None, safe=False)

@csrf_exempt
def saveClicks(request):
    global global_user_name
    req = request.POST.dict()
    print("here", req)
    toggle = eval(req["log"])["clicked"]
    try:
        season = req["log"]["season"]
    except:
        season = "TEST"
    now = datetime.now()
    types = "clicked"
    save_user_data = QuquLogs(
        user_name = global_user_name,
        toggle = toggle,
        season = season,
        date_time = now,
        types = types
    )
    save_user_data.save()
    return JsonResponse(None, safe=False)