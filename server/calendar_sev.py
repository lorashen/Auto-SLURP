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

datep=re.compile(r"202\d-\d\d-\d\d")
timep=re.compile(r"(202\d-\d\d-\d\d )*\d\d:\d\d[( am)|( pm)|( AM)|(( PM))]*")
@app.route("/calendar", methods=["GET", "POST"])
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
                print("失败，缺少参数：")
                return_dict = {'code': 'FAIL', 'msg': '失败，缺少参数：' + param}
                return return_dict
        intent = data.get('intent')
        #iid = str(data.get('iid'))
        if "event_name" in data: 
          slots["event_name"] = data.get('event_name')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "person" in data:
          slots["person"] = data.get('person')
        if "relation" in data:
          slots["relation"] = data.get('relation')
        if "date" in data:
          slots["date"] = data.get('date')
        #if "timeofday" in data:
        #  slots["timeofday"] = data.get('timeofday')
        if "time" in data:
          slots["time"] = data.get('time')
        if "from_time" in data:
          slots["from_time"] = data.get('from_time')
        if "to_time" in data:
          slots["to_time"] = data.get('to_time')
        if "time2" in data:
          slots["time2"] = data.get('time2')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        if "event_name" in request.args:
            slots["event_name"] = request.args.get('event_name')
        if "descriptor" in request.args:
            slots["descriptor"] = request.args.get('descriptor')
        if "person" in request.args:
            slots["person"] = request.args.get('person')
        if "relation" in request.args:
            slots["relation"] = request.args.get('relation')
        if "date" in request.args:
            slots["date"] = request.args.get('date')
        if "time" in request.args:
            slots["time"] = request.args.get('time')
        if "from_time" in request.args:
            slots["from_time"] = request.args.get('from_time')
        if "to_time" in request.args:
            slots["to_time"] = request.args.get('to_time')
        if "time2" in request.args:
            slots["time2"] = request.args.get('time2')

    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent =="calendar_set":
            if "time" not in slots:
                response="what time do you want to set the event?"
    elif intent =="calendar_query":
            if len(slots)==0:
                response="all the events are listed here. event 1: time:...."
            else:
                response="find 1 result. event index: 11, event time: ...."
    elif intent=="calendar_remove":
            if len(slots)==0:
                response="do you want to delete all the events?"
    else:
            response="not supporting intent"
    for key,value in slots.items() :
            if key.find("time")!=-1:
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
