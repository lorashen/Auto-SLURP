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
@app.route("/recommendation", methods=["GET", "POST"])
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
        if "business_type" in data: 
          slots["business_type"] = data.get('business_type')
        if "food_type" in data: 
          slots["food_type"] = data.get('food_type')
        if "movie_type" in data: 
          slots["movie_type"] = data.get('movie_type')
        if "place_name" in data: 
          slots["place_name"] = data.get('place_name')
        if "event_name" in data: 
          slots["event_name"] = data.get('event_name')
        if "movie_name" in data: 
          slots["movie_name"] = data.get('movie_name')
        if "date" in data: 
          slots["date"] = data.get('date')
        if "descriptor" in data: 
          slots["descriptor"] = data.get('descriptor')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "business_type" in data: 
          slots["business_type"] = data.get('business_type')
        if "food_type" in data: 
          slots["food_type"] = data.get('food_type')
        if "movie_type" in data: 
          slots["movie_type"] = data.get('movie_type')
        if "place_name" in data: 
          slots["place_name"] = data.get('place_name')
        if "event_name" in data: 
          slots["event_name"] = data.get('event_name')
        if "movie_name" in data: 
          slots["movie_name"] = data.get('movie_name')
        if "date" in data: 
          slots["date"] = data.get('date')
        if "descriptor" in data: 
          slots["descriptor"] = data.get('descriptor')


    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent =="recommendation_events":
            response="find 10 results. event ..., content: ...."
    elif intent =="recommendation_movies":
            response="find 10 results. movie ..., content: ...."
    elif intent=="recommendation_locations":
            if len(slots)==0:
                response="what kind of locations are you looking for?"
            else:
                response="find 10 results. location ..., introduction: ...."
    else:
            response="unsupported intent"
    for key,value in slots.items() :
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
