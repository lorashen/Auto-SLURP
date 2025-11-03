import sys
import re
import csv
from datetime import date,timedelta
from openai import OpenAI
def resolve(slot):
    pos=slot.find("place_name")
    if pos!=-1:
        bgpos=slot[pos:].find(":")
        citypos=slot[pos+bgpos:].find("'")
        oldcity=slot[pos+bgpos+1:pos+bgpos+citypos]
        oldcity=oldcity.strip()
        if oldcity=="my city":
            newcity="new york"
            slot=slot[:pos+bgpos+1]+str(newcity)+slot[pos+bgpos+citypos:]
    pos=slot.find("date")
    if pos!=-1:
        bgpos=slot[pos:].find(":")
        datepos=slot[pos+bgpos:].find("'")
        olddate=slot[pos+bgpos+1:pos+bgpos+datepos]
        olddate=olddate.strip()
        today=date.today()
        #today=date.fromisoformat("2025-05-14")
        weekday=date.isoweekday(today)% 7
        #print(today)
        #print(weekday)
        newdate2=None
        if olddate=="today":
            newdate=str(today)
        elif olddate=="tomorrow":
            newdate=today+timedelta(days=1)
        elif olddate=="this week":
            weekday=date.isoweekday(today)% 7
            newdate2=today+ timedelta(days=7-weekday)
            newdate=today-timedelta(days=weekday-1)
        elif olddate=="last week":
            weekday=date.isoweekday(today)% 7
            newdate2=today-timedelta(days=weekday)
            newdate=today-timedelta(days=weekday+6)

        elif olddate=="this weekend":
            weekday=date.isoweekday(today)% 7
            newdate=today+timedelta(days=6-weekday)
            newdate2=today+timedelta(days=7-weekday)
        elif olddate=="sunday":
            weekday=date.isoweekday(today)% 7
            newdate=today+timedelta(7-weekday)
        elif olddate=="august fifteenth":
            if str(today).find("-")!=-1:
                ypos=str(today).find("-")
                newdate=str(today)[:ypos+1]+"08-15"
            else:
                newdate="08-15"
        else:
           newdate=olddate
        #print(slot)
        slot=slot[:pos+bgpos+1]+str(newdate)+slot[pos+bgpos+datepos:]
        if newdate2:
            slot=slot+",'date2:"+str(newdate2)+"'"
        #print(slot)
    pos=slot.find("timeofday")
    oldtimeofday=""
    if pos!=-1:
        bgpos=slot[pos:].find(":")
        datepos=slot[pos+bgpos:].find("'")
        oldtimeofday=slot[pos+bgpos+1:pos+bgpos+datepos]
        oldtimeofday=oldtimeofday.strip()
        cpos=slot[pos:].rfind(",")
        if cpos!=-1:
            slot=slot[:cpos]+slot[pos+bgpos+datepos+1:]
        else:
            cpos=slot[pos:].find(",")
            if cpos==-1:
                cbpos=slot[:pos].rfind(",")
                if cbpos==-1:
                    slot=slot[:pos]+slot[pos+bgpos+datepos+1:]
                else:
                    slot=slot[:cbpos]+slot[pos+bgpos+datepos+1:]
            else:
                slot=slot[:pos]+slot[cpos+1:]
    pos=slot.find("time:")
    if pos==-1:
        pos=slot.find("time :")
    if pos!=-1:
        bgpos=slot[pos:].find(":")
        timepos=slot[pos+bgpos:].find("'")
        oldtime=slot[pos+bgpos+1:pos+bgpos+timepos]
        oldtime=oldtime.strip()
        newtime=oldtime.replace("five","05:00").replace("six","06:00").replace("nine","09:00").replace("ten","10:00").replace("three","3:00").replace("one","1:00")
        if not(newtime.endswith("am") or newtime.endswith("pm")):
            if oldtimeofday=="morning":
                newtime=newtime+" am"
            elif oldtimeofday=="evening":
                newtime=newtime+" pm"
            elif oldtimeofday.find("afternoon")!=-1:
                newtime=newtime+" pm"
        #print(slot)
        slot=slot[:pos]+"time:"+str(newtime)+slot[pos+bgpos+timepos:]
        #print(slot)
    else:
        if oldtimeofday.find("afternoon")!=-1:
            newtime="15:00"
            #print(slot)
            slot=slot+",'time:'"+newtime
            #print(slot)
    pos=slot.find("time2:")
    if pos==-1:
        pos=slot.find("time2 :")
    if pos!=-1:
        bgpos=slot[pos:].find(":")
        timepos=slot[pos+bgpos:].find("'")
        oldtime=slot[pos+bgpos+1:pos+bgpos+timepos]
        oldtime=oldtime.strip()
        newtime=oldtime.replace("five","05:00").replace("six","06:00").replace("nine","09:00").replace("ten","10:00").replace("three","3:00").replace("one","1:00")
        if not(newtime.endswith("am") or newtime.endswith("pm")):
            if oldtimeofday=="morning":
                newtime=newtime+" am"
            elif oldtimeofday=="evening":
                newtime=newtime+" pm"
            elif oldtimeofday.find("afternoon")!=-1:
                newtime=newtime+" pm"
        #print(slot)
        slot=slot[:pos]+"to_time:"+str(newtime)+slot[pos+bgpos+timepos:]
        slot=slot.replace("'time:","'from_time:")
            

    return slot
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
        slot=row[3]
        slot=slot.strip('[]')
        slot=resolve(slot)
        query={"iid":iid,"query":row[1],"intent":row[2],"slot":slot}#,"slots":slot,"domain":row[4]}
        queries.append(query)
    return queries
if __name__=="__main__":
    datep=re.compile(r"(======)*202[45]-\d\d-\d\d")
    client = OpenAI(base_url="https://api.deepseek.com/v1",api_key="")
    tasks=read_data("~/data/test.csv")
    intp=re.compile(r"intent:[a-z_]+")
    resp=re.compile(r"\{\"code\":\"SUCCESS\",\"data\".+\}")
    for i in range(0,100):
        print("-----*****------")
        print(i)
        data=[]
        with open(str(i)+".log") as f:
            lines=f.readlines()

            for line in lines:
                if datep.match(line):
                    continue
                else:
                    data.append(line)

        content="\n".join(data)
        intentf=intp.search(content)
        if intentf:
            intent=intentf.group(0)
            if intent.find("weather")!=-1 or intent.find("news_query")!=-1 or intent.find("qa")!=-1 or intent.find("stock")!=-1 or intent.find("general")!=-1 or intent.find("currency")!=-1:
                print("ChatCompletionMessage(content='')")
                #pass
            else:
                resf= resp.findall(content)
                if resf:
                    res=resf[-1]
                    msg=[{"role": "system", "content":"please judge the following result is right or wrong. if slot is {} and result also {}, it is right. if slot are same, it is right. If slot value are same, but slot name are not, then it is wrong. The slot time_zone and place_name are different, and can not be neglected. If intent is datetime_query, then the slot date:"+str(date.today())+" can be neglected. Other intent: The difference of slot change_to and change_amount can not be neglected even their value are the same. if time is same, no matter if has am/pm, it is right. The slot setting can not be neglected. If slot music_genre or event_name has difference, then can neglect it. if slot is descriptor:all, then can neglect it, but if result event_name is not null, then can not neglect. other descriptor can not neglect. For the slot list_name, if has same meaning, then can neglect. the slot person is same with slot from_person and to_person. if slot is query:song name, can be neglected. if the place_name is New York, it can be neglected. the place_name will be resolved, so if it is added by state name and country name, it is right. Please choose <Right> or <Wrong>"},{"role":"user", "content":"The golden slot is :{"+tasks[i]["slot"]+"}. The result is "+res}],
                    print(msg)
                    completion = client.chat.completions.create(
                      model="deepseek-chat",
                      temperature=0.0,
                      messages=[{"role": "system", "content":"please judge the following result is right or wrong. if slot is {} and result also {}, it is right. if slot are same, it is right. If slot value are same, but slot name are not, then it is wrong. The slot time_zone and place_name are different, and can not be neglected. If intent is datetime_query, then the slot date:"+str(date.today())+" can be neglected. Other intent: The difference of slot change_to and change_amount can not be neglected even their value are the same. if time is same, no matter if has am/pm, it is right. The slot setting can not be neglected. If slot music_genre or event_name has difference, then can neglect it. if slot is descriptor:all, then can neglect it, but if result event_name is not null, then can not neglect. other descriptor can not neglect. For the slot list_name, if has same meaning, then can neglect. The slot person is same with slot from_person and to_person. if slot is query:song name, can be neglected. if the place_name is New York, it can be neglected. the place_name will be resolved, so if it is added by state name and country name, it is right. Please choose <Right> or <Wrong>."},{"role":"user", "content":"The golden slot is :{"+tasks[i]["slot"]+"}. The result is "+res}],
                    )
                    print(completion.choices[0].message)
                else:
                    print("ChatCompletionMessage(content='the result is <Wrong>')")
                    continue
        else:
            if content.find("\"results\"")==-1 and content.find("\"data\"")==-1 and content.find("\"success\"")==-1:
                print("ChatCompletionMessage(content='the result is <Wrong>. no server response.')")
                continue
        goldintent=tasks[i]["intent"]
        if goldintent.find("weather")!=-1 or goldintent.find("news_query")!=-1 or goldintent.find("qa")!=-1 or goldintent.find("stock")!=-1 or goldintent.find("general")!=-1 or goldintent.find("currency")!=-1:
          msg=[{"role": "system", "content":"please judge the following content finish the task is right or wrong. Must has the server response ,if not, it's wrong. if intent is general_quirky,  if it's a general_greet or chit-chat like 'are you happy', and there is no chat reply to user, it is wrong. If intent is weather_query, need to provide the weather condition, and if no weather condition, it is wrong. if intent is qa, the response need to provide the answer to the question, and if only provide url, it is wrong. if intent is news, whole_manager need to response detail of the news. if ask for currency, the result need provide the conversion rate, the currency name may be Proper Noun, it is right. also need to check if the annotaion are the same with server response. Please choose <Right> or <Wrong>."},{"role": "user", "content": "the task is "+tasks[i]["query"]+". The annotation is "+tasks[i]["slot"]+"\n"+"\n".join(data)+"\nyour answer is :"}],
          print(msg)
          try:
              completion = client.chat.completions.create(
                model="deepseek-chat",
                temperature=0.0,
                messages=[{"role": "system", "content":"please judge the following content finish the task is right or wrong. Must has the server response ,if not, it's wrong. if intent is general_quirky, if it's a general_greet or chit-chat like 'are you happy', and there is no chat reply to user, it is wrong. If intent is weather_query, need to provide the weather condition, and if no weather condition, it is wrong. if intent is qa, the response need to provide the infomation to the question, and if only provide url, it is wrong. if intent is news, whole_manager need to response detail of the news. if ask for currency, the result need provide the conversion rate, the currency name may be Proper Noun, it is right. also need to check if the annotaion are the same with server response. Please choose <Right> or <Wrong>."},{"role": "user", "content": "the task is "+tasks[i]["query"]+". The annotation is "+tasks[i]["slot"]+"\n"+"\n".join(data)+"\nyour answer is :"}],
              )

              print(completion.choices[0].message)
          except:
              completion = client.chat.completions.create(
                model="deepseek-chat",
                temperature=0.0,
                messages=[{"role": "system", "content":"please judge the following content finish the task is right or wrong. Must has the server response ,if not, it's wrong. if intent is general_quirky, if it's a general_greet or chit-chat like 'are you happy', and there is no chat reply to user, it is wrong. If intent is weather_query, need to provide the weather condition, and if no weather condition, it is wrong. if intent is qa, the response need to provide the answer to the question, and if only provide url, it is wrong. if intent is news, whole_manager need to response detail of the news. if ask for currency, the result need provide the conversion rate, the currency name may be Proper Noun, it is right. also need to check if the annotaion are the same with server response. Please choose <Right> or <Wrong>."},{"role": "user", "content": "the task is "+tasks[i]["query"]+". The annotation is "+tasks[i]["slot"]+"\n"+"\n".join(data)[-16000:]+"\nyour answer is :"}],
              )
              print(completion.choices[0].message)


        else:
          msg=[{"role": "system", "content":"please judge the following content finish the task is right or wrong. Must has the server response {\"code\":\"SUCCESS\"},if not, it's wrong. if response is not supported intent, it is wrong. If response is format not right, it is wrong. If the server response need further more information, it is right. If the response fake some infomation that the user did not provide, it is wrong. Please choose <Right> or <Wrong>."},{"role": "user", "content": "the task is "+tasks[i]["query"]+". The annotation is "+tasks[i]["slot"]+"\n"+"\n".join(data)+"\nyour answer is :"}],
          print(msg)
          completion = client.chat.completions.create(
            model="deepseek-chat",
            temperature=0.0,
            messages=[{"role": "system", "content":"please judge the following content finish the task is right or wrong. Must has the server response {\"code\":\"SUCCESS\"},if not, it's wrong. if response is not supported intent, it is wrong. If response is format not right, it is wrong. If the server response need further more information, it is right. If the response fake some infomation that the user did not provide, it is wrong. Please choose <Right> or <Wrong>."},{"role": "user", "content": "the task is "+tasks[i]["query"]+". The annotation is "+tasks[i]["slot"]+"\n"+"\n".join(data)+"\nyour answer is :"}],
          )

          print(completion.choices[0].message)

          

