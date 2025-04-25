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
@app.route("/email", methods=["GET", "POST"])
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
        if "setting" in data: 
          slots["setting"] = data.get('setting')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "person" in data:
          slots["person"] = data.get('person')
        if "to_person" in data:
          slots["to_person"] = data.get('to_person')
        if "from_person" in data:
          slots["from_person"] = data.get('from_person')
        if "relation" in data:
          slots["relation"] = data.get('relation')
        if "to_relation" in data:
          slots["to_relation"] = data.get('to_relation')
        if "from_relation" in data:
          slots["from_relation"] = data.get('from_relation')
        if "email_folder" in data:
          slots["email_folder"] = data.get('email_folder')
        if "content" in data:
          slots["content"] = data.get('content')
        if "time" in data:
          slots["time"] = data.get('time')
        if "date" in data:
          slots["date"] = data.get('date')
        if "email_address" in data:
          slots["email_address"] = data.get('email_address')
        if "app_name" in data:
          slots["app_name"] = data.get('app_name')
        if "query" in data:
          slots["query"] = data.get('query')
        if "personal_info" in data:
          slots["personal_info"] = data.get('personal_info')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "setting" in data: 
          slots["setting"] = data.get('setting')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "person" in data:
          slots["person"] = data.get('person')
        if "to_person" in data:
          slots["to_person"] = data.get('to_person')
        if "from_person" in data:
          slots["from_person"] = data.get('from_person')
        if "relation" in data:
          slots["relation"] = data.get('relation')
        if "to_relation" in data:
          slots["to_relation"] = data.get('to_relation')
        if "from_relation" in data:
          slots["from_relation"] = data.get('from_relation')
        if "email_folder" in data:
          slots["email_folder"] = data.get('email_folder')
        if "content" in data:
          slots["content"] = data.get('content')
        if "time" in data:
          slots["time"] = data.get('time')
        if "date" in data:
          slots["date"] = data.get('date')
        if "email_address" in data:
          slots["email_address"] = data.get('email_address')
        if "app_name" in data:
          slots["app_name"] = data.get('app_name')
        if "query" in data:
          slots["query"] = data.get('query')
        if "personal_info" in data:
          slots["personal_info"] = data.get('personal_info')

    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent=="email_sendemail":
            if "to_person" not in slots and "person" not in slots and "relation" not in slots and "to_relation" not in slots:
                response="need provide the recipient."
    elif intent=="email_addcontact":
            if "email_address" not in slots:
                response="need provide email address."
    elif intent=="email_query":
            if len(slots)==0:
                response="what kind of email do you want to search for?"
            else:
                response="find 1 result. email index: 12, email content: hi, how's going?...."
    elif intent=="email_querycontact":
            response="find 1 result. the contact index: 8, information is: name...."
    elif intent=="email_subscription":
            if len(slots)==0:
                response="what kind of email do you want me to watch?"
    elif intent=="email_remove":
            if len(slots)==0:
                response="what kind of email do you want to delete?"
    else:
            response="not supporting intent"
    for key,value in slots.items() :
            if key=="time":
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
