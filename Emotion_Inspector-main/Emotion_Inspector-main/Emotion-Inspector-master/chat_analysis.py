import re
import text2emotion as te
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import warnings
warnings.filterwarnings('ignore')

# Extract the Date time
def date_time(s):
    pattern='^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]? -'
    result=re.match(pattern, s)
    if result:
        return True
    return False 

# Extract contacts
def find_contact(s):
    s=s.split(":")
    if len(s)==2:
        return True
    else:
        return False

    
# Extract Message
def getMassage(line):
    splitline=line.split(' - ')
    datetime= splitline[0];
    date, time= datetime.split(', ')
    message=" ".join(splitline[1:])
    
    if find_contact(message):
        splitmessage=message.split(": ")
        author=splitmessage[0]
        message=splitmessage[1]
    else:
        author=None
    return date, time, author, message

data=[]
conversation='../input/chatdata2/chatdata (2).txt'
with open(conversation, encoding="utf-8") as fp:
    fp.readline()
    messageBuffer=[]
    date, time, author= None, None, None
    while True:
        line=fp.readline()
        if not line:
            break
        line=line.strip()
        if date_time(line):
            if len(messageBuffer) >0:
                data.append([date, time, author, ''.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message=getMassage(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

df=pd.DataFrame(data, columns=["Date", "Time", "contact", "Message"])
df['Date']=pd.to_datetime(df['Date'])

data=df.dropna()

sentiments=SentimentIntensityAnalyzer()
data["Happy"]= [te.get_emotion(i)["Happy"] for i in data["Message"]]
data["Angry"]= [te.get_emotion(i)["Angry"] for i in data["Message"]]
data["Surprise"]= [te.get_emotion(i)["Surprise"] for i in data["Message"]]
data["Sad"]= [te.get_emotion(i)["Sad"] for i in data["Message"]]
data["Fear"]= [te.get_emotion(i)["Fear"] for i in data["Message"]]

data

a = sum(data["Happy"])
b = sum(data["Angry"])
c = sum(data["Surprise"])
d = sum(data["Sad"])
e = sum(data["Fear"])

scores = [a,b,c,d,e]

def sentiment_score(a, b, c, d, e):
    maxval = max(scores)
    if maxval == a:
        print("Happy 😄")
    elif maxval == b:
        print("Angry 😡")
    elif maxval == c:
        print("Surprise 😲")
    elif maxval == d:
        print("Sad 😔")
    else:
        print("Fear 😨")
sentiment_score(a,b,c,d,e)

data['temp_list'] = data['Message'].apply(lambda x:str(x).split())
top = Counter([item for sublist in data['temp_list'] for item in sublist])
temp = pd.DataFrame(top.most_common(15))
temp.columns = ['Common_words','count']
temp.style.background_gradient(cmap='Blues')

fig = px.bar(temp, x="count", y="Common_words", title='Most Commmon Words', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()