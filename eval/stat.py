import re
wrong=0
right=0
wrongcount=0
rightcount=0
judgesent=re.compile(r"ChatCompletionMessage")
with open("eval.log") as f:
    lines=f.readlines()
    for line in lines:
        lowline=line.lower()
        if line.startswith("-----**"):
            if wrong>0:
                wrongcount+=1
            elif right>0:
                rightcount+=1
            else:
                print("error")
            wrong=0
            right=0
        elif judgesent.match(line):
            if lowline.find("wrong")!=-1 or lowline.find("incorrect")!=-1 or lowline.find("not completed")!=-1:
                wrong+=1
            elif lowline.find("right")!=-1 or lowline.find("correct")!=-1:
                right+=1
            elif lowline.find("content=''")!=-1:
                pass
            else:
                print("error")
    if wrong>0:
        wrongcount+=1
    else:
        rightcount+=1
acc=float(rightcount)/100
print(acc,"right",rightcount,"wrong",wrongcount)
