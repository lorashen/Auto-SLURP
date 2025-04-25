import os 

from typing import List

from agentlite.actions import BaseAction, FinishAct, ThinkAct
from agentlite.agents import BaseAgent
from agentlite.commons import TaskPackage
from agentlite.llm.agent_llms import get_llm_backend, LLMConfig
from agentlite.llm.agent_llms import BaseLLM
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
class IntentAgent(BaseAgent):
    def __init__(
        self, llm: BaseLLM, actions: List[BaseAction] = [], **kwargs
    ):
        name = "IntentAgent"
        role = "read the examples and results, copy iid and predict intent for the sentence. for 'iid:7199,query:set the alarm to two pm' first predict the domain, as domain:alarm, then copy the iid from query,iid:7199, then the intent and slots, as the format: intent:alarm_set,time:two pm. the intents are calendar:calendar_set,calendar_remove,calendar_query\n\
lists:lists_query,lists_remove,lists_createoradd\n\
music:play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query\n\
news:news_query,news_subscription\n\
alarm:alarm_set,alarm_query,alarm_remove,alarm_change\n\
email:email_sendemail,email_query,email_querycontact,email_subscription,email_addcontact,email_remove\n\
iot:iot_hue_lightcolor,iot_hue_lightother,iot_coffee,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down\n\
weather:weather_query\n\
datetime:datetime_query,datetime_convert\n\
stock:qa_stock\n\
qa:qa_factoid,general_quirky,qa_definition,general_joke,qa_maths\n\
greet:general_greet\n\
currency:qa_currency\n\
transport:transport_taxi,transport_ticket,transport_query,transport_traffic\n\
recommendation:recommendation_events,recommendation_movies,recommendation_locations\n\
podcast:play_podcasts\n\
audiobook:play_audiobook\n\
radio:play_radio,radio_query\n\
takeaway:takeaway_query,takeaway_order\n\
social:social_query,social_post\n\
cooking:cooking_recipe\n\
phone:phone_text,phone_notification\n\
game:play_game\
"
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
agent_actions = []
agent = BaseAgent(
    name=agent_info["name"],
    role=agent_info["role"],
    llm=llm,
    actions=agent_actions,
    #reasoning_type="react",
)
prompt="the examples and results:  {"iid": "7499", "query": "turn up"}	iid:7499,intent:audio_volume_up\n {"iid": "6811", "query": "what's the current weather"}	iid:6811,intent:weather_query\ni want you to remind me the next meeting with my girlfriend it will be at eight pm next sunday	intent:calendar_set,event_name : meeting,relation:girlfriend, time : eight pm, date : next Sunday\ncancel alarm for tenth of march two thousand seventeen	intent:alarm_remove,date : tenth of march two thousand seventeen\nhave you heard any good jokes lately	intent:general_joke\nget it fast resolved	intent:social_post\nalexa book me a train ticket for this afternoon to chicago	intent:transport_ticket,transport_type : train, timeofday : this afternoon, place_name : chicago\ni did not want you to send that text yet wait until i say send	intent:email_sendemail,setting:save\nwhat causes if i had junk food and alcohols	intent:general_quirky,content:what causes if i had junk food and alcohols\nfind a recipe for a romantic dinner for two	intent:cooking_recipe,food_descriptor: romantic dinner for two\nplease turn up the lights in this room	intent:iot_hue_lightup,house_place:this room\nwhats happening in pop industry	intent:news_query	,news_topic : pop industry\nis today the fourth or the fifth	intent:datetime_query,date : today\nthe wemo plug should be turned off on	intent:iot_wemo_off,device_type : wemo plug\nwhen i get home can you please order a pizza	intent:takeaway_order,food_type : pizza\nfind the events	intent:recommendation_events\nstart radio and go to frequency on one thousand and forty eight	intent:play_radio,radio_name : one thousand and forty eight\ni want to listen arijit singh song once again	intent:play_music,artist_name : arijit singh\nplease arrange to wake me up at three am alarm	intent:alarm_set,time : three am\nstart dune from where i left off	intent:play_audiobook,player_setting : resume, audiobook_name : dune\n please return the result of this sentence: "
FLAG_CONTINUE = True
while FLAG_CONTINUE:
    input_text = input("Ask Intent Agent question:\n")
    task = TaskPackage(instruction=prompt+"\n"+input_text)
    agent(task)
    if input("Do you want to continue? (y/n): ") == "n":
        FLAG_CONTINUE = False
'''
