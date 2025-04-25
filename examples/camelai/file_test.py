from camel.societies.workforce import Workforce

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from datetime import date, datetime
import requests
import json
import csv
import sys
import asyncio
# Define the model, here in this case we use gpt-4o-mini
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4,
    model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
)
from camel.agents import ChatAgent
pmsys_msg="you are controlling smart home system, you have intentagent, timeagent, locationagent, urlagent, and requestagent to complete the user's task. You should first use intentagent to complete the intent prediction. Then if the result has time or location params, please try to ask timeagent or locationagent to solve the time and location. At last you should use requestagent to send and receive request from other servers such as weather server and response to user to finalize the task."
intentsys_msg="read the examples and results, copy iid and predict intent for the sentence. for 'iid:7199,query:set the alarm to two pm' first predict the domain, as domain:alarm, then copy the iid from query,iid:7199, then the intent and slots, as the format: intent:alarm_set,time:two pm. the intents are calendar:calendar_set,calendar_remove,calendar_query\n\
lists:lists_query,lists_remove,lists_createoradd\n\
music:play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query\n\
news:news_query,news_subscription\n\
alarm:alarm_set,alarm_query,alarm_remove,alarm_change\n\
email:email_sendemail,email_query,email_querycontact,email_subscription,email_addcontact,email_remove\n\
iot:iot_hue_lightchange,iot_coffee,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down\n\
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
timesys_msg="read time params, and convert to formated time. if has date, call the time_tool getdate function to get date, format should be year-month-date. the time is 10:00. if has time, the time format should be 10:00. this morning the time will be 10:00, this afternoon the time will be 15:00"
locationsys_msg="read the location params, and convert to formated location. current location is new york."
urlsys_msg="read the params, and choose the function to send and receive the requests. iid should also be string. choose the url from the provided servers' url list:\
                qa server is http://api.serpstack.com/search? access_key = {key}& query = {query}\n\
                news query server is http://api.mediastack.com/v1/news?access_key={key}&keywords={keyword}&date={date}&sort=published_desc\n\
                news subscription server http://127.0.0.1:3020/news,intent(news_subscription),iid,news_topic,\
                weather server first request https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=10&language=en&format=json to get latitude and latitude, then request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&models=gfs_seamless\n\
                stock server is first to get the stock symbol http://api.serpstack.com/search? access_key = {key}& query = {name} stock symbol , then request to this server http://api.marketstack.com/v1/eod? access_key = {key}& symbols = {symbol}&limit=5\n\
                currency server is https://www.amdoren.com/api/currency.php?api_key={key}&from={currency}&to={currency2}&amount={amount}\n\
                http://127.0.0.1:3000/alarm, intent(alarm_query,alarm_set),iid,event_name,descriptor,time,from_time,to_time,\
                http://127.0.0.1:3001/audiobook,intent(play_audiobook), iid,player_setting,house_place,media_type,descriptor,audiobook_name,author_name,\
                http://127.0.0.1:3002/calendar,intent(calendar_query,calendar_remove,calendar_set),iid,event_name,descriptor,person,relation,date,time,from_time,to_time,\
                http://127.0.0.1:3003/cooking,intent(cooking_recipe),iid,food_type,descriptor,\
                http://127.0.0.1:3004/datetime,intent(datetime_convert,datetime_query),iid,place_name,descriptor,time_zone,time_zone2,date,time,time2,\
                http://127.0.0.1:3005/email,intent(email_query,email_sendemail),iid,setting,person,to_person,from_person,relation,to_relation,from_relation,email_folder,time,date,email_address,app_name,query,content,personal_info,\
                http://127.0.0.1:3006/game,intent(play_game),iid,game_name,\
                http://127.0.0.1:3007/iot,intent(iot_coffee,iot_hue_lightchange,iot_hue_lightdim,iot_hue_lightup,audio_volume_mute,iot_hue_lightoff,audio_volume_up,iot_wemo_off,audio_volume_other,iot_cleaning,iot_wemo_on,audio_volume_down),iid,device_type,house_place,time,color_type,change_amount,item_name,setting,\
                http://127.0.0.1:3008/lists,intent(lists_query,lists_remove,lists_createoradd),iid,list_name,item_name,descriptor,time,date,\
                http://127.0.0.1:3009/music,intent(play_music,music_likeness,playlists_createoradd,music_settings,music_dislikeness,music_query),iid,player_setting,descriptor,artist_name,song_name,playlist_name,music_genre,query,\
                http://127.0.0.1:3010/phone,intent(phone_text,phone_notification),iid,device_type,event_name,text,\
                http://127.0.0.1:3011/podcasts,intent(play_podcasts),iid,podcast_name,player_setting,podcast_descriptor,\
                http://127.0.0.1:3013/radio,intent(play_radio,radio_query),iid,radio_name,app_name,person_name,music_genre,device_type,house_place,player_setting,descriptor,query,time,\
                http://127.0.0.1:3014/recommendation,intent(recommendation_events,recommendation_movies,recommendation_locations),iid,business_type,food_type,movie_type,movie_name,date,place_name,event_name,descriptor,\
                http://127.0.0.1:3015/social,intent(social_query,social_post),iid,media_type,person,business_name,content,date,descriptor,\
                http://127.0.0.1:3017/takeaway,intent(takeaway_query,takeaway_order),iid,food_type,order_type,business_type,business_name,place_name,date,time,descriptor,\
                http://127.0.0.1:3018/transport,intent(transport_taxi,transport_ticket,transport_query,transport_traffic),iid,transport_agency,transport_type,business_type,business_name,place_name,to_place_name,from_place_name,query,date,time,descriptor,\
                then all the url format should be http://127.0.0.1:3002/calendar?intent=calendar_remove&event_name=meeting"
requestsys_msg="for qa, news query, weather, stock, and currency, just use the url. for other request, use the url and generate params, params should be json format, like this{\"intent\": \"calendar_remove\", \"event_name\": \"haircut appointment\", \"date\": \"2024-11-20\"}. choose the function to call. Then call the function and receive the response from the server."
response_msg="analyse the result from server, and generate response for the user."
def getdate() -> str:
    r"""request the date.


    Returns:
        string: The response.
    """
    from datetime import date, datetime
    results = date.today()
    return str(results)

from camel.toolkits import FunctionTool
time_tool = FunctionTool(getdate)

timeagent = ChatAgent(
    system_message=timesys_msg,
    model=model,
    tools=[time_tool],
    message_window_size=10, # [Optional] the length for chat memory
    )

def req(url: str ) -> str:
    r"""request the url.

    Args:
        url (str): URL for the new :class:`Request` object.

    Returns:
        string: The response of the server.
    """
    response=requests.get(url)
    print(response.text)
    '''
    else:
        response = requests.post(url, data=params)

        # 打印返回结果
        print(response.text)
        result=""
        if response.status_code >= 400:
            print(params)#["iid"])
            #result="code "+str(response.status_code)+"."
            response = requests.post(url, data=json.dumps(params))
            if response.status_code >= 400:
                result="code "+str(response.status_code)+"."
        else:
            pass
            res=json.loads(response.text)
            if res["data"]["response"]=="true":
                count+=1
                result="true"
            else:
                print(params)#["iid"])
                result="false"
            print(res["data"]["response"])
    '''
    return response.text


# Wrap the function with FunctionTool
#req_withquery_tool = FunctionTool(req_withquery)
req_tool = FunctionTool(req)

pmagent = ChatAgent(
    system_message=pmsys_msg,
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )
intentagent = ChatAgent(
    system_message=intentsys_msg,
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )
locationagent = ChatAgent(
    system_message=locationsys_msg,
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )
urlagent = ChatAgent(
    system_message=urlsys_msg,
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )
requestagent = ChatAgent(
    system_message=requestsys_msg,
    model=model,
    tools=[req_tool],
    message_window_size=10, # [Optional] the length for chat memory
    )
responseagent = ChatAgent(
    system_message=response_msg,
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
    )

# Create a workforce instance
workforce = Workforce("A Simple Workforce")
# Add the worker agent to the workforce
workforce.add_single_agent_worker(
    "An agent that can do program manage",
    worker=pmagent,
)
workforce.add_single_agent_worker(
    "An agent that can predict intent and key info",
    worker=intentagent,
).add_single_agent_worker(
    "An agent that can provide date and time and format it",
    worker=timeagent,
).add_single_agent_worker(
    "An agent that can provide location and format it",
    worker=locationagent,
).add_single_agent_worker(
    "An agentthat can provide the url and query",
    worker=urlagent,
).add_single_agent_worker(
    "An agentthat can make request to the server and receive the response",
    worker=requestagent,
).add_single_agent_worker(
    "An agentthat can analyse the server result and generate response, this agent will finish the whole task",
    worker=responseagent,
)
from camel.tasks import Task#,TaskState

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
  for sent in tasks:
    print("---------*****************************************-----------")
    #test_sent = json.dumps(sent)
    print(sent["iid"])

    # the id of the task can be any string to mark the task
    task = Task(
        content=sent["query"],
        #alexa lights brighter",
        #book me a train ticket for this afternoon to chicago",#add dentist appointment for friday at five",#what's the weather today?",
        id="0",
    )
    try:
        task = workforce.process_task(task)
        print(task.result)
    except:
        pass
        #if task.state == TaskState.FAILED:
        #asyncio.run(workforce._handle_failed_task(task))
