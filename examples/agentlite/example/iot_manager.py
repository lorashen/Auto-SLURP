# get llm backend
from agentlite.llm.agent_llms import get_llm_backend
from agentlite.llm.LLMConfig import LLMConfig
import csv
import sys
import json

llm_config_dict = {
    "llm_name": "gpt-4",#3.5-turbo-16k-0613",
    "temperature": 0.0,
     "api_key": "",
}
llm_config = LLMConfig(llm_config_dict)
llm = get_llm_backend(llm_config)

# define the individual agents
from IntentAgent import IntentAgent
from TimeAgent import TimeAgent


from LocationAgent import LocationAgent
from ExecAgent import ExecAgent


intent_agent = IntentAgent(llm)
time_agent = TimeAgent(llm)
location_agent = LocationAgent(llm)
excution_agent = ExecAgent(llm)


# define the manager agent
from agentlite.agents import ManagerAgent

manager_agent_info = {
    "name": "whole_manager",
    "role": "you are controlling smart home system, you have intent_agent, time_agent, location_agent, and excution_agent to complete the user's task. You should first use intent_agent to complete the intent prediction. Then if the result has time or location params, please try to ask time_agent or location_agent to solve the time and location. If has currency name, you should convert the currency name to the name in the currency map. At last you should use excution_agent to send and receive request from other servers such as weather server and response to user to finalize the task. If the server's response is need further information, need to response to the user that need infomation, and your task is finished.",
}
iot_manager = ManagerAgent(
    llm,
    manager_agent_info["name"],
    manager_agent_info["role"],
    TeamAgents=[intent_agent, time_agent,location_agent,currency_agent,excution_agent],
)

# test the manager agent with TaskPackage
from agentlite.commons import TaskPackage

def read_data(file_path):
    queries=[]
    with open(file_path, newline='') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
      count=0
      for row in spamreader:
        if count==0:
            count+=1
            continue
        #print(row[2])
        #print(len(row))
        iid=row[0]
        query={"iid":iid,"query":row[1]}#,"slots":slot,"domain":row[4]}
        queries.append(query)
    return queries

if __name__=="__main__":
  tasks=read_data("~/data/test.csv")
  #print(tasks)
  index = int(sys.argv[1])
  tasks=tasks[index:index+1]
  for task in tasks:
  #for task in tasks:
    test_task = json.dumps(task)
    test_task_pack = TaskPackage(instruction=test_task, task_creator="User")
    response = iot_manager(test_task_pack)
    print(response)
#test_task = "set notification from world news"
'''
test_task = "what is the weather today"
test_task_pack = TaskPackage(instruction=test_task, task_creator="User")
response = iot_manager(test_task_pack)
print(response)
