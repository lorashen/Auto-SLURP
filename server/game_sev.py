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

@app.route("/game", methods=["GET", "POST"])
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
            return_dict = {'code': 'FAIL', 'msg': 'fail, missing parameters'}
            return return_dict
        params = ['intent', ]
        for param in params:
            if param not in data:
                return_dict = {'code': 'FAIL', 'msg': 'fail, missing parameters: ' + param}
                return return_dict
        intent = data.get('intent')
        #iid = str(data.get('iid'))
        if "game_name" in data: 
          slots["game_name"] = data.get('game_name')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "game_name" in data: 
          slots["game_name"] = data.get('game_name')

    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent=="play_game":
            if len(slots)==0:
                response="which game do you want to play?"
    else:
            response="not supporting intent"
    print('time: ' + str(time.time()-start_time))
    print('----------------------')
    return_dict = {}
    return_dict['code'] = 'SUCCESS'
    return_dict['msg'] = 'success'
    contents = {}
    contents['response'] = response
    contents['query'] = query
    return_dict['data'] = contents
    return return_dict
        
print("finish loading")

if __name__ == "__main__":
        print("start---------")
        port = sys.argv[1]
        app.run(debug=False, host='0.0.0.0',port=port)
        print("startup completed---------")
