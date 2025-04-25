import os

import wikipedia
import duckduckgo_search

from agentlite.actions.BaseAction import BaseAction
import requests
import json

class ExecAction(BaseAction):
    def __init__(self) -> None:
        #action_name = "request"
        #action_desc = "Using this action to request servers."
        #params_doc = {"url": "the request url.","query":"the request content, json format."}
        super().__init__(
            action_name="request", action_desc="Using this action to request servers.", params_doc={"url": "the request url.","query":"if news or weather or qa or stock or currency server, then empty query. json format, like this{\"intent\": \"calendar_remove\", \"iid\": \"7890\", \"event_name\": \"haircut appointment\", \"date\": \"2024-11-20\"}"},
        )
        print(self.action_name)

    def __call__(self, url,query):
      if url.find("mediastack")!=-1 or url.find("meteo")!=-1 or url.find("marketstack")!=-1:
        response=requests.get(url)
        print(response.text)
      else:
        response = requests.post(url, data=query)

        # 打印返回结果
        print(response.text)
        result=""
        if response.status_code >= 400:
            print(query)#["iid"])
            result="code "+str(response.status_code)+"."
        else:
            pass
            '''
            res=json.loads(response.text)
            if res["data"]["response"]=="true":
                count+=1
                result="true"
            else:
                print(query)#["iid"])
                result="false"
            print(res["data"]["response"])
            '''
      return response.text
