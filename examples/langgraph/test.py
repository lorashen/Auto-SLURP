from typing import Annotated, List

from langchain_core.tools import tool
from datetime import date, datetime
import requests
from typing_extensions import TypedDict
import csv
import sys
import json
@tool
def time_tool() -> str:
    """get today's date"""
    results = date.today()
    return str(results)


@tool
def request_tool(url: Annotated[str, "the url to be requested"]) -> str:
    """send request using get method to the url"""
    response=requests.get(url)
    print(response.text)
    return response.text


from typing import List, Optional
from typing_extensions import Literal
from langchain_core.language_models.chat_models import BaseChatModel

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage, trim_messages


def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers to finish the first user's cmd: {members}. Given the following user request,"
        " respond with the worker to act next. you are controlling smart home system, you have intent, time, location, and url agent and request to complete the user's task. You should first use intent to complete the intent prediction. Then if the result has time or location params, please try to ask time or location to solve the time and location. At last you should choose the url using url agent, and then use request to send and receive request to the url such as weather server and then use genresponse to generate response, then finalize the task. Even if the request's response is need further information or is a question, do not further answer the question, just finish the task."
        " The response need to be the worker to act next, for example: {\"next\": \"FINISH\"}. When finished,"
        " respond with FINISH. the data in json."
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    def supervisor_node(state: MessagesState) -> Command[Literal[*members, "__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        print(response)
        goto = json.loads(response)["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto)

    return supervisor_node


from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(model="gpt-4",temperature=0)
#llm = ChatOpenAI(model="gpt-4o",temperature=0)
#json_llm = llm.bind(response_format={"type": "json_object"})
#structured_llm = llm.with_structured_output(method="json_mode", include_raw=True)
intent_agent = create_react_agent(llm, tools=[],state_modifier=(
        "read the examples and results, predict intent for the sentence. for 'set the alarm to two pm', first predict the domain, as domain:alarm, then the intent and slots, as the format: intent:alarm_set,time:two pm.\n\
The intents are calendar:calendar_set,calendar_remove,calendar_query\n\
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
game:play_game\n\
"
        "Don't ask follow-up questions. data in json."
    )
)
time_agent = create_react_agent(llm, tools=[time_tool],state_modifier=(
        "You are a time agent. Read the time params in slots, and convert to formated time. if has date, call the time_tool to get today's date. Then calculate the date according to today's date. The time is 10:00. If has time, the time format should be 10:00."
        "Don't try to answer the first question directly. Don't ask follow-up questions. data in json."
    )
)
request_agent = create_react_agent(llm, tools=[request_tool],state_modifier=(
    "Always call the request_tool to request the url and get the response from the server"
    "data in json."
    )
)


def intent_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = intent_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="intent")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )
def time_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = time_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="time")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )
def request_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = request_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="request")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )


location_agent = create_react_agent(llm, tools=[], state_modifier=(
    "You are a location agent. Read the location params in slots, and convert to formated location. if location is in house, do not need to resolve. current location is new york."
    "Don't ask follow-up questions. data format in json."
    )
)
#                currency server is https://www.amdoren.com/api/currency.php?api_key={key}&from={currency}&to={currency2}&amount={amount}\n\
url_agent = create_react_agent(llm, tools=[], state_modifier=(
    "You are a url agent. Read the params in intent and slots, then choose the url from the servers' url list. also need to modify the slot name to the url description:\
                qa server is http://api.serpstack.com/search?access_key={key}&query={query}\n\
                news query server is http://api.mediastack.com/v1/news?access_key={key}&keywords={keyword}&date={date}&sort=published_desc\n\
                news subscription server http://127.0.0.1:3020/news,intent(news_subscription),iid,news_topic,\
                weather server first request https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=10&language=en&format=json to get latitude and latitude, then request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,rain_sum,showers_sum,snowfall_sum,wind_speed_10m_max\n\
                stock server is first to get the stock symbol http://api.serpstack.com/search? access_key = {key}& query = {name} stock symbol , then request to this server http://api.marketstack.com/v1/eod? access_key = {key}& symbols = {symbol}&limit=5\n\
                currency server is https://api.freecurrencyapi.com/v1/latest?apikey={key}&base_currency={currency}&currencies={currency2}\n\
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
                then all the url format should be http://127.0.0.1:3002/calendar?intent=calendar_remove&event_name=meeting\n\
    data in json."
    )
)
response_agent = create_react_agent(llm, tools=[], state_modifier=(
    "You are a genresponse agent. Read the content, and generate response to the first user's cmd. The format should be 'response':'...'"
    "Don't ask follow-up questions. data format in json."
    )
)


def location_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = location_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="location")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )

def url_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = url_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="url")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )

def response_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = response_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="genresponse")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )

research_supervisor_node = make_supervisor_node(llm, ["intent", "time", "location", "url", "request", "genresponse"])

research_builder = StateGraph(MessagesState)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("intent", intent_node)
research_builder.add_node("time", time_node)
research_builder.add_node("location", location_node)
research_builder.add_node("url", url_node)
research_builder.add_node("request", request_node)
research_builder.add_node("genresponse", response_node)

research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()
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

    for s in research_graph.stream(
      {"messages": [("user", task["query"])]},
      {"recursion_limit": 100},
    ):
      print(s)
      print("---")
