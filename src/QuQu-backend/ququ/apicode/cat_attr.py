from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen , Request
import json 
from ququ.models import *
from django.db import connection
from ququ.apicode.FashionFormer.detect import *

def make_result(year, season):
    result = {}
    # common_attribute 
    result['common_attributes'] = list(QuquCommonAttributes.objects.filter(year=year, season=season).values())
    cat_attr = list(QuquCatAttr.objects.filter(year=year, season=season).values())
    result['cat_attr'] = {}
    result['cat_attr']['category'] = []
    result['cat_attr']['attribute'] = []
    cursor = connection.cursor()
    trend_attribute = list(QuquTrendAttributes.objects.filter(year=year, season=season).values())[0]["attributes"].split("|")
    trend_category = [x.split("_")[0] for x in trend_attribute]
    for c_a in cat_attr:
        query_res_cat = list(QuquCategory.objects.filter(id=c_a['category']).values())
        ccc = query_res_cat[0]["id"]
        if str(ccc) in trend_category:
            query_res_cat[0]["free"] = 0
        else:
            query_res_cat[0]["free"] = 1
        result['cat_attr']['category'].append(query_res_cat)
        if (len(c_a['attribute']) > 0):
            sql_regexp = list(map(lambda x: "^"+x+"$", c_a['attribute'].split('|')))
            sql = "select distinct * from ququ_attributes where id regexp '" +  "|".join( sql_regexp ) + "'"
            cursor.execute(sql)
            rows = [x for x in cursor]
            cols = [x[0] for x in cursor.description]
            songs = []
            for row in rows:
                sss = "{}_{}".format(ccc, row[1])
                song = {}
                for prop, val in zip(cols, row):
                    song[prop] = val
                if sss in trend_attribute:
                    song["free"] = 0
                else:
                    song["free"] = 1
                songs.append(song)
            result['cat_attr']['attribute'].append(songs) 
        else: 
            result['cat_attr']['attribute'].append(query_res_cat)   

    colors = list(ColorLabel.objects.values())
    result['color'] = {}
    result['color']['category'] = []
    result['color']['attribute'] = []
    temp_dict= {}
    for a in colors:
        index_label = a["index"]
        tone_label = a["label"].split("_")[0]
        color_label = a["label"].split("_")[1]
        rgb_label = []
        for i in a["RGB"].lstrip("[").rstrip("]").split(" "):
            if i.isnumeric():
                rgb_label.append(i)
        rgb_label = str("(" + ",".join(rgb_label) + ")")
        tttt = {}
        tttt["index"] = index_label
        tttt["id"] = color_label
        tttt["name"] = color_label
        tttt["rgb"] = rgb_label
        if tone_label in temp_dict:
            temp_dict[tone_label].append(tttt)
        else:
            temp_dict[tone_label] = []
            temp_dict[tone_label].append(tttt)
    for a in temp_dict:
        songs = []
        song = {}
        song["index"] = 0
        song["id"] = a
        song["name"] = a
        song["free"] = 0

        songs.append(song)
        result['color']['category'].append(songs)
        songss = []
        for b in temp_dict[a]:
            b["free"] = 0

            songss.append(b)
        result['color']['attribute'].append(songss)
    brand_list = list(QuquBrandAtt.objects.filter(year=year, season=season).values())
    brand = []
    
    for i in brand_list:
        brand.append(i["brand"])
    result["brand"] = "|".join(brand)

    return result

def make_result2(brand_list):
    result = {}
    for i in brand_list.split("|"):
        a = i.split("_")[0]
        b = i.split("_")[1]
        if a.isnumeric():
            c_n = list(QuquCategory.objects.filter(id=a).values())[0]["name"]
            if b == '':
                a_n == ''
            else:
                a_n = list(QuquAttributes.objects.filter(id=b).values())[0]["name"]
            if c_n not in result:
                result[c_n] = []
                result[c_n].append(a_n)
            else:
                result[c_n].append(a_n)
        else :
            if a not in result:
                result[a] = []
                result[a].append(b)
            else:
                result[a].append(b)
    return result

def run_detection(url, global_user_name):
    images = start_model(url, global_user_name)
    
    return images