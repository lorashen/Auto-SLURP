import os 

from typing import List
from ExecAction import ExecAction
from agentlite.actions import BaseAction, FinishAct, ThinkAct
from agentlite.agents import BaseAgent
from agentlite.commons import TaskPackage
from agentlite.commons import AgentAct
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
class ExecAgent(BaseAgent):
    def __init__(
        self, llm: BaseLLM, actions: List[BaseAction] = [ExecAction()], **kwargs
    ):
        name = "ExecAgent"
        role = "read the params, and send and receive the requests. iid should also be string. choose the url from the servers' url list:\
                qa server is http://api.serpstack.com/search?access_key={key}&query={query}\n\
                news query server is http://api.mediastack.com/v1/news?access_key={key}&keywords={keyword}&date={date}&sort=published_desc\n\
                news subscription server http://127.0.0.1:3020/news,intent(news_subscription),iid,news_topic,\
                weather server first request https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=10&language=en&format=json to get latitude and latitude, then request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,rain_sum,showers_sum,snowfall_sum,wind_speed_10m_max\n\
                stock server is first to get the stock symbol http://api.serpstack.com/search? access_key = {key}& query = {name} stock symbol , then request to this server http://api.marketstack.com/v1/eod? access_key = {key}& symbols = {symbol}&limit=5\n\
                currency server is https://www.amdoren.com/api/currency.php?api_key={key}&from={currency}&to={currency2}&amount={amount}\n\
                http://127.0.0.1:3000/alarm, intent(alarm_query,alarm_set),iid,event_name,descriptor,time,from_time,to_time,\
                http://127.0.0.1:3001/audiobook,intent(play_audiobook), iid,player_setting,house_place,media_type,descriptor,audiobook_name,author_name,\
                http://127.0.0.1:3002/calendar,intent(calendar_query,calendar_remove,calendar_set),iid,event_name,descriptor,person,relation,date,time,from_time,to_time,\
                http://127.0.0.1:3003/cooking,intent(cooking_recipe),iid,food_type,descriptor,\
                http://127.0.0.1:3004/datetime,intent(datetime_convert,datetime_query),iid,place_name,descriptor,time_zone,time_zone2,date,time,time2,\
                http://127.0.0.1:3005/email,intent(email_query,email_sendemail),iid,setting,person,to_person,from_person,relation,to_relation,from_relation,email_folder,time,date,email_address,app_name,query,content,personal_info,\
                http://127.0.0.1:3006/game,intent(play_game),iid,game_name,\
                http://127.0.0.1:3007/iot,intent(iot_coffee,iot_hue_lightcolor,iot_hue_lightother,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down),iid,device_type,house_place,time,color_type,change_amount,change_to,item_name,setting,\
                http://127.0.0.1:3008/lists,intent(lists_query,lists_remove,lists_createoradd),iid,list_name,item_name,descriptor,time,date,\
                http://127.0.0.1:3009/music,intent(play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query),iid,player_setting,descriptor,artist_name,song_name,playlist_name,music_genre,query,\
                http://127.0.0.1:3010/phone,intent(phone_text,phone_notification),iid,device_type,event_name,text,\
                http://127.0.0.1:3011/podcasts,intent(play_podcasts),iid,podcast_name,player_setting,podcast_descriptor,\
                http://127.0.0.1:3013/radio,intent(play_radio,radio_query),iid,radio_name,app_name,person_name,music_genre,device_type,house_place,player_setting,descriptor,query,time,\
                http://127.0.0.1:3014/recommendation,intent(recommendation_events,recommendation_movies,recommendation_locations),iid,business_type,food_type,movie_type,movie_name,date,place_name,event_name,descriptor,\
                http://127.0.0.1:3015/social,intent(social_query,social_post),iid,media_type,person,business_name,content,date,descriptor,\
                http://127.0.0.1:3017/takeaway,intent(takeaway_query,takeaway_order),iid,food_type,order_type,business_type,business_name,place_name,date,time,descriptor,\
                http://127.0.0.1:3018/transport,intent(transport_taxi,transport_ticket,transport_query,transport_traffic),iid,transport_agency,transport_type,business_type,business_name,place_name,to_place_name,from_place_name,query,date,time,descriptor,\
"
        super().__init__(
            name=name, role=role, llm=llm, actions=actions, logger=agent_logger
        )
        self.__build_examples__()

    def __build_examples__(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # an example of search agent with wikipedia api call
        # task
        task = "intent:set_notification"


                # 2. api call action and obs
        act_params = {}
        act_1 = AgentAct(name=ExecAction().action_name, params=act_params)
        obs_1 = "OK"
        '''
        # 3. think action and obs
        thought = "I find salesforce is Founded by former Oracle executive Marc Benioff in February 1999"
        act_3 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_3 = "OK"

        # 4. finish action
        answer = "February 1999"
        act_4 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: answer})
        obs_4 = "Task Completed."

        task_pack = TaskPackage(instruction=task)
        act_obs = [(act_1, obs_1), (act_2, obs_2), (act_3, obs_3), (act_4, obs_4)]
        self.add_example(task=task_pack, action_chain=act_obs)
        '''
def test_search_agent():
    llm_config_dict = {"llm_name": "gpt-4", "temperature": 0.1}
    actions = [ExecAction()]
    llm_config = LLMConfig(llm_config_dict)
    # print(llm_config.__dict__)
    llm = get_llm_backend(llm_config)
    ## test the one-shot wikipedia search agent
    labor_agent = ExecAgent(llm=llm)
    # labor_agent = DuckSearchAgent(llm=llm)

    test_task = "intent:set_notification, news_category:world news"
    test_task_pack = TaskPackage(instruction=test_task)
    response = labor_agent(test_task_pack)
    print("response:", response)


if __name__ == "__main__":
    test_search_agent()

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
