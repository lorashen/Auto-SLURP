# coding=utf-8
from flask import Flask, request 
import json 
import os
import sys
import time
import csv
import re
app=Flask(__name__)

def read_chat_intents_from_file(file_path,domain):
    queries = dict()
    with open(file_path ) as f:
      lines=f.readlines()
      count=0
      for line in lines:
        line=line.strip()
        query=json.loads(line)
        if query['domain']==domain:
            queries[query["iid"]]=query

    return queries

timep=re.compile(r"\d\d:\d\d[( am)|( pm)|( AM)|(( PM))]*")
@app.route("/iot", methods=["GET", "POST"])
def check():
    intent=""
    slots=dict()
    start_time = time.time()
    if request.method == "POST":
        jsondata = request.get_data(as_text=True)
        if jsondata:
            data = json.loads(jsondata)
            print(data)
        else:
            return_dict = {'code': 'FAIL', 'msg': '失败，缺少参数'}
            return return_dict
        params = ['intent', ]
        for param in params:
            if param not in data:
                return_dict = {'code': 'FAIL', 'msg': '失败，缺少参数：' + param}
                return return_dict
        intent = data.get('intent')
        #iid = str(data.get('iid'))
        if "device_type" in data: 
          slots["device_type"] = data.get('device_type')
        if "house_place" in data:
          slots["house_place"] = data.get('house_place')
        if "change_amount" in data:
          slots["change_amount"] = data.get('change_amount')
        if "change_to" in data:
          slots["change_to"] = data.get('change_to')
        if "color_type" in data:
          slots["color_type"] = data.get('color_type')
        if "item_name" in data:
          slots["item_name"] = data.get('item_name')
        if "setting" in data:
          slots["setting"] = data.get('setting')
        if "time" in data:
          slots["time"] = data.get('time')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "device_type" in data: 
          slots["device_type"] = data.get('device_type')
        if "house_place" in data:
          slots["house_place"] = data.get('house_place')
        if "change_amount" in data:
          slots["change_amount"] = data.get('change_amount')
        if "change_to" in data:
          slots["change_to"] = data.get('change_to')
        if "color_type" in data:
          slots["color_type"] = data.get('color_type')
        if "item_name" in data:
          slots["item_name"] = data.get('item_name')
        if "setting" in data:
          slots["setting"] = data.get('setting')
        if "time" in data:
          slots["time"] = data.get('time')


    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent =="iot_hue_lightcolor":
            pass
    elif intent =="iot_coffee" or intent =="audio_volume_mute" or intent =="iot_hue_lightoff" or intent =="iot_wemo_off" or intent =="iot_cleaning" or intent =="iot_wemo_on":
            pass
    elif intent=="iot_hue_lightdim" or intent=="iot_hue_lightup":
            if "change_amount" not in slots:
                response="change the lights with default amount."
    elif intent=="iot_hue_lightchange":
            if "change_to" not in slots:
                response="change the lights to default."
    elif intent=="audio_volume_up" or intent=="audio_volume_down":
            if "change_amount" not in slots:
                response="change the volume with default amount."
    elif intent =="audio_volume_other":
            if "change_to" not in slots:
                response="change the volume to default."
    else:
            response="not supporting intent"
    for key,value in slots.items() :
            if key.find("time")!=-1:
                if timep.match(value) is None:
                    response="time format not right"
    print('耗时：' + str(time.time()-start_time))
    print('----------------------')
    return_dict = {}
    return_dict['code'] = 'SUCCESS'
    return_dict['msg'] = '成功'
    contents = {}
    contents['response'] = response
    contents['query'] = query
    return_dict['data'] = contents
    return return_dict
        
print("模型load完毕")

if __name__ == "__main__":
        print("启动开始---------")
        port = sys.argv[1]
        app.run(debug=False, host='0.0.0.0',port=port)
        print("启动完成---------")
