import autogen
from autogen import ConversableAgent, UserProxyAgent, config_list_from_json
import requests
from typing_extensions import Annotated
from datetime import date, datetime

import csv
import sys
import json
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list}

time_assistant = autogen.AssistantAgent(
    name="Time_assistant",
    system_message="Read the time params, and convert to formated time. If has date, call the user_proxy_auto get_time function to get today's date, then calculate and format the date mentioned in the params. The time is 10:00. If has time, the time format should be 10:00. If no time specify, can return default time. If no date and time params, just skip.",
    llm_config=llm_config,
)
location_assistant = autogen.AssistantAgent(
    name="Location",
    system_message="Read the location params, and convert to formated location. The current location is new york.",
    llm_config=llm_config,
)
intent_assistant = autogen.AssistantAgent(
    name="intent",
    llm_config=llm_config,
    system_message="\
        Read the examples and results, and predict intent for the sentence. For 'set the alarm to two pm', first predict the domain, as domain:alarm, then the intent and slots, as the format: intent:alarm_set,time:two pm. \n\
the intents are calendar:calendar_set,calendar_remove,calendar_query\n\
lists:lists_query,lists_remove,lists_createoradd\n\
music:play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query\n\
news:news_query,news_subscription\n\
alarm:alarm_set,alarm_query,alarm_remove,alarm_change\n\
email:email_sendemail,email_query,email_querycontact,email_subscription,email_addcontact,email_remove\n\
iot:iot_hue_lightother,iot_hue_lightcolor,iot_coffee,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down\n\
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
",
)
#old currency server                currency server is https://www.amdoren.com/api/currency.php?api_key={key}&from={currency}&to={currency2}&amount={amount}\n\
url_assistant = autogen.AssistantAgent(
    name="url_assistant",
    system_message="Read the params, and choose the url from the servers' url list:\
                qa server is http://api.serpstack.com/search?access_key={key}&query={query}\n\
                news query server is http://api.mediastack.com/v1/news?access_key={key}&keywords={keyword}&date={date}&sort=published_desc\n\
                news subscription server http://214.10.10.4:3020/news,intent(news_subscription),news_topic,\
                weather server first request https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=10&language=en&format=json to get latitude and latitude, then request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&models=gfs_seamless\n\
                stock server is first to get the stock symbol http://api.serpstack.com/search?access_key={key}&query={name} stock symbol , then request to this server http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}&limit=5\n\
                currency server is https://api.freecurrencyapi.com/v1/latest?apikey={key}&base_currency={currency}&currencies={currency2}\n\
                http://214.10.10.4:3000/alarm, intent(alarm_query,alarm_set),event_name,descriptor,time,from_time,to_time,\
                http://214.10.10.4:3001/audiobook,intent(play_audiobook), player_setting,house_place,media_type,descriptor,audiobook_name,author_name,\
                http://214.10.10.4:3002/calendar,intent(calendar_query,calendar_remove,calendar_set),event_name,descriptor,person,relation,date,time,from_time,to_time,\
                http://214.10.10.4:3003/cooking,intent(cooking_recipe),food_type,descriptor,\
                http://214.10.10.4:3004/datetime,intent(datetime_convert,datetime_query),place_name,descriptor,time_zone,time_zone2,date,time,time2,\
                http://214.10.10.4:3005/email,intent(email_query,email_sendemail),setting,person,to_person,from_person,relation,to_relation,from_relation,email_folder,time,date,email_address,app_name,query,content,personal_info,\
                http://214.10.10.4:3006/game,intent(play_game),game_name,\
                http://214.10.10.4:3007/iot,intent(iot_coffee,iot_hue_lightchange,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down),device_type,house_place,time,color_type,change_to,change_amount,item_name,setting,\
                http://214.10.10.4:3008/lists,intent(lists_query,lists_remove,lists_createoradd),list_name,item_name,descriptor,time,date,\
                http://214.10.10.4:3009/music,intent(play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query),player_setting,descriptor,artist_name,song_name,playlist_name,music_genre,query,\
                http://214.10.10.4:3010/phone,intent(phone_text,phone_notification),device_type,event_name,text,\
                http://214.10.10.4:3011/podcasts,intent(play_podcasts),podcast_name,player_setting,podcast_descriptor,\
                http://214.10.10.4:3013/radio,intent(play_radio,radio_query),radio_name,app_name,person_name,music_genre,device_type,house_place,player_setting,descriptor,query,time,\
                http://214.10.10.4:3014/recommendation,intent(recommendation_events,recommendation_movies,recommendation_locations),business_type,food_type,movie_type,movie_name,date,place_name,event_name,descriptor,\
                http://214.10.10.4:3015/social,intent(social_query,social_post),media_type,person,business_name,content,date,descriptor,\
                http://214.10.10.4:3017/takeaway,intent(takeaway_query,takeaway_order),food_type,order_type,business_type,business_name,place_name,date,time,descriptor,\
                http://214.10.10.4:3018/transport,intent(transport_taxi,transport_ticket,transport_query,transport_traffic),transport_agency,transport_type,business_type,business_name,place_name,to_place_name,from_place_name,query,date,time,descriptor,\n\
                then all the url format should be http://214.10.10.4:3002/calendar?intent=calendar_remove&event_name=meeting",
    #generate url and query (url, query). query should be json format, like this\"{\\\"intent\\\": \\\"calendar_remove\\\", \\\"iid\\\": \\\"7890\\\", \\\"event_name\\\": \\\"haircut appointment\\\", \\\"date\\\": \\\"2024-11-20\\\"}\". \
#",
    llm_config=llm_config,
)
#request_assistant = autogen.AssistantAgent(
#    name="Request",
'''
    system_message="read the params, and send and receive the requests. iid should also be string. choose the url from the servers' url list:\
                qa server is http://api.serpstack.com/search? access_key = {key}& query = {query}\n\
                news query server is http://api.mediastack.com/v1/news?access_key={key}&keywords={keyword}&date={date}&sort=published_desc\n\
                news subscription server http://214.10.10.4:3020/news,intent(news_subscription),iid,news_topic,\
                weather server first request https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=10&language=en&format=json to get latitude and latitude, then request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&models=gfs_seamless\n\
                stock server is first to get the stock symbol http://api.serpstack.com/search? access_key = {key}& query = {name} stock symbol , then request to this server http://api.marketstack.com/v1/eod? access_key = {key}& symbols = {symbol}&limit=5\n\
                currency server is https://www.amdoren.com/api/currency.php?api_key={key}&from={currency}&to={currency2}&amount={amount}\n\
                http://214.10.10.4:3000/alarm, intent(alarm_query,alarm_set),iid,event_name,descriptor,time,from_time,to_time,\
                http://214.10.10.4:3001/audiobook,intent(play_audiobook), iid,player_setting,house_place,media_type,descriptor,audiobook_name,author_name,\
                http://214.10.10.4:3002/calendar,intent(calendar_query,calendar_remove,calendar_set),iid,event_name,descriptor,person,relation,date,time,from_time,to_time,\
                http://214.10.10.4:3003/cooking,intent(cooking_recipe),iid,food_type,descriptor,\
                http://214.10.10.4:3004/datetime,intent(datetime_convert,datetime_query),iid,place_name,descriptor,time_zone,time_zone2,date,time,time2,\
                http://214.10.10.4:3005/email,intent(email_query,email_sendemail),iid,setting,person,to_person,from_person,relation,to_relation,from_relation,email_folder,time,date,email_address,app_name,query,content,personal_info,\
                http://214.10.10.4:3006/game,intent(play_game),iid,game_name,\
                http://214.10.10.4:3007/iot,intent(iot_coffee,iot_hue_lightchange,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down),iid,device_type,house_place,time,color_type,change_amount,item_name,setting,\
                http://214.10.10.4:3008/lists,intent(lists_query,lists_remove,lists_createoradd),iid,list_name,item_name,descriptor,time,date,\
                http://214.10.10.4:3009/music,intent(play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query),iid,player_setting,descriptor,artist_name,song_name,playlist_name,music_genre,query,\
                http://214.10.10.4:3010/phone,intent(phone_text,phone_notification),iid,device_type,event_name,text,\
                http://214.10.10.4:3011/podcasts,intent(play_podcasts),iid,podcast_name,player_setting,podcast_descriptor,\
                http://214.10.10.4:3013/radio,intent(play_radio,radio_query),iid,radio_name,app_name,person_name,music_genre,device_type,house_place,player_setting,descriptor,query,time,\
                http://214.10.10.4:3014/recommendation,intent(recommendation_events,recommendation_movies,recommendation_locations),iid,business_type,food_type,movie_type,movie_name,date,place_name,event_name,descriptor,\
                http://214.10.10.4:3015/social,intent(social_query,social_post),iid,media_type,person,business_name,content,date,descriptor,\
                http://214.10.10.4:3017/takeaway,intent(takeaway_query,takeaway_order),iid,food_type,order_type,business_type,business_name,place_name,date,time,descriptor,\
                http://214.10.10.4:3018/transport,intent(transport_taxi,transport_ticket,transport_query,transport_traffic),iid,transport_agency,transport_type,business_type,business_name,place_name,to_place_name,from_place_name,query,date,time,descriptor,\n\
    generate url and query then call the url function. the function params are (url, query). query should be json format, like this\"{\\\"intent\\\": \\\"calendar_remove\\\", \\\"iid\\\": \\\"7890\\\", \\\"event_name\\\": \\\"haircut appointment\\\", \\\"date\\\": \\\"2024-11-20\\\"}\". for url request, use the functions you have been provided with.",
'''
request_assistant = autogen.AssistantAgent(
    name="Request",
    system_message="for url and query params, use the request functions you have been provided with.",
    llm_config=llm_config,
)
genresponse_assistant = autogen.AssistantAgent(
    name="GenResponse",
    system_message="generate response for the user use server response.",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="you are controlling smart home system, you have intent assistant, time_assistant, location_assistant, url_assistant and request_assistant to complete the user's task. You should first use intent to complete the intent prediction. Then if the result has time or location params, please try to ask time_assistant or location_assistant to solve the time and location. Then you choose the url using url_assistant. At last you should use request_assistant to send and receive request through functions from other servers such as weather server and response to user. You should generates reponse for the user, and tell manager to finalize the task.",
    llm_config=llm_config,
)
user_proxy_auto = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    default_auto_reply="if finish task, TERMINATE. If not, solve again.",
    #is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    #code_execution_config={
    #    "last_n_messages": 0,
    #    "work_dir": "tasks",
    #    "use_docker": False,
    #},  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    system_message="Also execute the function and report the result.",
)
#    system_message="you are controlling smart home system, you have intent, time_assistant, location_assistant, url_assistant and request_assistant, genresponse_assistant to complete the user's task. You should first use intent to complete the intent prediction. Then if the result has time or location params, please try to ask time_assistant or location_assistant to solve the time and location. Then you choose the url using url_assistant. At last you should use request_assistant to send and receive request through functions from other servers such as weather server and use genresponse assistant to generate response to user according to the server result to finalize the task.",
#)

@user_proxy_auto.register_for_execution()
@time_assistant.register_for_llm(description="get today's date.")
def get_time():
    results = date.today()
    return str(results)

@user_proxy_auto.register_for_execution()
@request_assistant.register_for_llm(description="url request execution.")
def url_request(
    url: Annotated[str, "url to request"],
) -> str:
    response=requests.get(url)
    print(response.text)
    result=""
    if response.status_code >= 400:
        result="code "+str(response.status_code)+"."
    else:
        pass

    return f"server response {response.text}"
'''
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="ALWAYS",  # ask human for input at each step
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)
'''
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

  #termination = TextMentionTermination("exit") # Type 'exit' to end the conversation.
  #team = RoundRobinGroupChat([web_surfer, assistant, user_proxy], termination_condition=termination)
  #await Console(team.run_stream(task="Find information about AutoGen and write a short summary."))
  groupchat = autogen.GroupChat(agents=[user_proxy_auto,pm, intent_assistant, time_assistant, location_assistant,  url_assistant, request_assistant], messages=[], max_round=12)
  manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config,system_message="Group Chat Manager. You should finalize the task after product manager generate response to user.")
  for task in tasks:
    test_task = json.dumps(task)
    #Console(manager.run_stream(task="Find information about AutoGen and write a short summary."))
    user_proxy_auto.initiate_chat(
       manager, message=test_task
    )
