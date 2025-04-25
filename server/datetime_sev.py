# coding=utf-8
from flask import Flask, request 
import json 
import os
import time
import csv
import sys
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

datep=re.compile(r"202\d-\d\d-\d\d")
timep=re.compile(r"(202\d-\d\d-\d\d )*\d\d:\d\d[( am)|( pm)|( AM)|(( PM))]*")
@app.route("/datetime", methods=["GET", "POST"])
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
        if "place_name" in data: 
          slots["place_name"] = data.get('place_name')
        if "place_name2" in data: 
          slots["place_name2"] = data.get('place_name2')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "date" in data:
          slots["date"] = data.get('date')
        if "time" in data:
          slots["time"] = data.get('time')
        if "time2" in data:
          slots["time2"] = data.get('time2')
        if "time_zone" in data:
          slots["time_zone"] = data.get('time_zone')
        if "time_zone2" in data:
          slots["time_zone2"] = data.get('time_zone2')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "place_name" in data: 
          slots["place_name"] = data.get('place_name')
        if "place_name2" in data: 
          slots["place_name2"] = data.get('place_name2')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "date" in data:
          slots["date"] = data.get('date')
        if "time" in data:
          slots["time"] = data.get('time')
        if "time2" in data:
          slots["time2"] = data.get('time2')
        if "time_zone" in data:
          slots["time_zone"] = data.get('time_zone')
        if "time_zone2" in data:
          slots["time_zone2"] = data.get('time_zone2')


    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent =="datetime_query":
        if len(slots)==0:
            response="Today is ...."
        else:
            response="The date and time is ...."
    elif intent =="datetime_convert":
            if "place_name" not in slots and "place_name2" not in slots and "time_zone" not in slots and "time_zone2" not in slots:
                response="which time zone you want to convert to?"
            else:
                response="the time is ...."
    else:
            response="not supporting intent"
    for key,value in slots.items() :
            if key=="time" or key=="time2":
                if timep.match(value) is None:
                    response="time format not right"
            if key.find("date")!=-1:
                if datep.match(value) is None:
                    response="date format not right"
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
