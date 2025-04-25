import os 

from typing import List
from intent_actions import get_intent,get_user_current_date, get_user_current_location, get_latitude_longitude
from agentlite.actions import BaseAction, FinishAct, ThinkAct
from agentlite.agents import BaseAgent
from agentlite.commons import TaskPackage
from agentlite.llm.agent_llms import get_llm_backend, LLMConfig
from agentlite.llm.agent_llms import BaseLLM
from intent_actions import get_intent,get_user_current_date, get_user_current_location, get_latitude_longitude

from TimeAction import TimeAction,CurDateAction
from agentlite.logging.terminal_logger import AgentLogger
agent_logger = AgentLogger(PROMPT_DEBUG_FLAG=False)
# LAM_URL = os.environ["LAM_URL"]
# print(LAM_URL)
# llm_config = LLMConfig(
#         {
#             "llm_name": "xlam_v2", 
#             "temperature": 0.0, 
#             "base_url": LAM_URL,
#             "api_key": "EMPTY"
#         }
#     )
llm_name = "gpt-4"#3.5-turbo"#-16k"#-0613"#gpt-4"
llm_config = LLMConfig({"llm_name": llm_name, "temperature": 0.0,
        "api_key": "",})
llm = get_llm_backend(llm_config)
class TimeAgent(BaseAgent):
    def __init__(
        self, llm: BaseLLM, actions: List[BaseAction] = [TimeAction(),CurDateAction()], **kwargs
    ):
        name = "TimeAgent"
        role = "read the time params, and convert to formated time with TimeAction. if has date, call the CurDateAction to get date, format should be 2024-11-20. the time is 10:00. if has time, the time format should be 10:00"
        super().__init__(
            name=name, role=role, llm=llm, actions=actions, logger=agent_logger
        )
        #self.__build_examples__()

    def __build_examples__(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # an example of search agent with wikipedia api call
        # task
        task = "send the email to this new email address"

        # 1. think action and obs
        thought = "I should first figure out the intent"
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = ""
'''
agent_actions = []#get_intent(),get_user_current_date(), get_user_current_location(), get_latitude_longitude()]#, get_weather_forcast()]
agent = BaseAgent(
    name=agent_info["name"],
    role=agent_info["role"],
    llm=llm,
    actions=agent_actions,
    #reasoning_type="react",
)
prompt="the examples and results: turn up	intent:audio_volume_up\nwhat's the current weather	intent:weather_query\ni want you to remind me the next meeting with my girlfriend it will be at eight pm next sunday	intent:calendar_set,event_name : meeting,relation:girlfriend, time : eight pm, date : next Sunday\ncancel alarm for tenth of march two thousand seventeen	intent:alarm_remove,date : tenth of march two thousand seventeen\nhave you heard any good jokes lately	intent:general_joke\nget it fast resolved	intent:social_post\nalexa book me a train ticket for this afternoon to chicago	intent:transport_ticket,transport_type : train, timeofday : this afternoon, place_name : chicago\ni did not want you to send that text yet wait until i say send	intent:email_sendemail,setting:save\nwhat causes if i had junk food and alcohols	intent:general_quirky,content:what causes if i had junk food and alcohols\nfind a recipe for a romantic dinner for two	intent:cooking_recipe,food_descriptor: romantic dinner for two\nplease turn up the lights in this room	intent:iot_hue_lightup,house_place:this room\nwhats happening in pop industry	intent:news_query	,news_topic : pop industry\nis today the fourth or the fifth	intent:datetime_query,date : today\nthe wemo plug should be turned off on	intent:iot_wemo_off,device_type : wemo plug\nwhen i get home can you please order a pizza	intent:takeaway_order,food_type : pizza\nfind the events	intent:recommendation_events\nstart radio and go to frequency on one thousand and forty eight	intent:play_radio,radio_name : one thousand and forty eight\ni want to listen arijit singh song once again	intent:play_music,artist_name : arijit singh\nplease arrange to wake me up at three am alarm	intent:alarm_set,time : three am\nstart dune from where i left off	intent:play_audiobook,player_setting : resume, audiobook_name : dune\n please return the result of this sentence: "
FLAG_CONTINUE = True
while FLAG_CONTINUE:
    input_text = input("Ask Intent Agent question:\n")
    task = TaskPackage(instruction=prompt+"\n"+input_text)
    agent(task)
    if input("Do you want to continue? (y/n): ") == "n":
        FLAG_CONTINUE = False
'''
