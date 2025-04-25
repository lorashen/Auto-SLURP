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

@app.route("/music", methods=["GET", "POST"])
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
        if "player_setting" in data: 
          slots["player_setting"] = data.get('player_setting')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "playlist_name" in data:
          slots["playlist_name"] = data.get('playlist_name')
        if "artist_name" in data:
          slots["artist_name"] = data.get('artist_name')
        if "song_name" in data:
          slots["song_name"] = data.get('song_name')
        if "music_genre" in data:
          slots["music_genre"] = data.get('music_genre')
        if "query" in data:
          slots["query"] = data.get('query')
    if request.method == "GET":
        if "intent" in request.args:
            intent = request.args.get("intent")
        data=request.args
        if "player_setting" in data: 
          slots["player_setting"] = data.get('player_setting')
        if "descriptor" in data:
          slots["descriptor"] = data.get('descriptor')
        if "playlist_name" in data:
          slots["playlist_name"] = data.get('playlist_name')
        if "artist_name" in data:
          slots["artist_name"] = data.get('artist_name')
        if "song_name" in data:
          slots["song_name"] = data.get('song_name')
        if "music_genre" in data:
          slots["music_genre"] = data.get('music_genre')
        if "query" in data:
          slots["query"] = data.get('query')


    response="operated successfully"
    query = {"intent":intent,"slots":slots}
    if intent =="play_music":
            if len(slots)==0:
                response="play random music."
    elif intent =="music_likeness" or intent=="music_dislikeness": 
            pass
    elif intent=="music_query":
            response="The song name is Imagine, it belongs to album Imagine, and the artist name is John Lennon."
    elif intent=="playlists_createoradd":
            if len(slots)==0:
                response="which song do you want to put in this playlist?"
    elif intent=="music_settings":
            if len(slots)==0:
                response="How do you want to set the music?"
    else:
            response="unsupported intent"
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
