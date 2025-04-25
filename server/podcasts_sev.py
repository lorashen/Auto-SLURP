# coding=utf-8
from flask import Flask, request 
import json 
import os
import time
import csv
import sys
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

@app.route("/podcasts", methods=["GET", "POST"])
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
        if "podcast_name" in data: 
          slots["podcast_name"] = data.get('podcast_name')
        if "player_setting" in data: 
          slots["player_setting"] = data.get('player_setting')
        if "podcast_descriptor" in data: 
          slots["podcast_descriptor"] = data.get('podcast_descriptor')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "podcast_name" in data: 
          slots["podcast_name"] = data.get('podcast_name')
        if "player_setting" in data: 
          slots["player_setting"] = data.get('player_setting')
        if "podcast_descriptor" in data: 
          slots["podcast_descriptor"] = data.get('podcast_descriptor')


    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent=="play_podcasts":
            if len(slots)==0:
                response="play random podcast."
    else:
            response="unsupported intent."
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
