from googleapiclient.discovery import build
from pymongo import MongoClient
from urllib.parse import quote_plus
import mysql.connector
import pandas as pd
import streamlit as st
import json
import pymongo
import warnings
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")


def fun():
    api_key = "AIzaSyCw34pbSpScIHWbyoiZPzEcXMzItfmdfmM"
    service = "youtube"
    version = "v3"
    tube = build(service, version, developerKey=api_key)
    return tube

youtube = fun()

# Getting channel info
def get_det(id):
    req = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=id
    )
    res = req.execute()
    for i in res["items"]:
        data = dict(
            channel_name=i["snippet"]["title"],
            id=i["id"],
            subscriber=i["statistics"]["subscriberCount"],
            tot_video=i["statistics"]["videoCount"],
            view_count=i["statistics"]["viewCount"],
            des=i["snippet"]["description"],
            playlist_id=i["contentDetails"]["relatedPlaylists"]["uploads"]
        )
    return data

# Getting video IDs
def video_id(id):
    req1 = youtube.channels().list(
        part="contentDetails",
        id=id
    )
    res1 = req1.execute()
    play_id = res1["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    next_page = None
    list1 = []
    while(True):
        req2 = youtube.playlistItems().list(
            part="snippet",
            playlistId=play_id,
            maxResults=50,
            pageToken=next_page
        )
        res2 = req2.execute()
        for i in res2["items"]:
            list1.append(i["snippet"]["resourceId"]["videoId"])
        next_page = res2.get("nextPageToken")
        if next_page is None:
            break
    return list1

# Getting video information
def video_info(video):
    l = []
    for i in video:
        req = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=i
        )
        res = req.execute()
        for j in res["items"]:
            data = dict(
                channel_name=j["snippet"]["channelTitle"],
                channel_id=j["snippet"]["channelId"],
                video_id=j["id"],
                tittle=j["snippet"]["title"],
                tag=j["snippet"].get("tags"),
                thumbnail=j["snippet"]["thumbnails"]["default"]["url"],
                des=j["snippet"].get("description"),
                pub_date=j["snippet"]["publishedAt"],
                duration=j["contentDetails"].get("duration"),
                views=j["statistics"].get("viewCount"),
                likes=j["statistics"].get("likeCount"),
                comments=j["statistics"].get("commentCount"),
                fav=j["statistics"]["favoriteCount"],
                defination=j["contentDetails"]["definition"],
                caption_status=j["contentDetails"]["caption"]
            )
            l.append(data)
    return l

# Getting comment information
def get_comment_info(video):
    l2 = []
    try:
        for id in video:
            req = youtube.commentThreads().list(
                part="snippet",
                videoId=id,
                maxResults=50
            )
            res = req.execute()
            for i in res["items"]:
                data = dict(
                    Comment_id=i["snippet"]["topLevelComment"]["id"],
                    video_id=i["snippet"]["topLevelComment"]["snippet"]["videoId"],
                    comment_text=i["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    comment_author=i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    comment_date=i["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                )
                l2.append(data)
    except:
        pass
    return l2

# Getting playlist info
def playlist_id(id):
    next_page = None
    l3 = []
    while True:
        req = youtube.playlists().list(
            part="snippet",
            channelId=id,
            maxResults=50,
            pageToken=next_page
        )
        res = req.execute()
        for i in res["items"]:
            data = dict(
                playlist_id=i["id"],
                tittle=i["snippet"]["title"],
                publish_date=i["snippet"]["publishedAt"],
                channel_id=i["snippet"]["channelId"],
                channel_name=i["snippet"]["channelTitle"]
            )
            l3.append(data)
        next_page = res.get("nextPageToken")
        if next_page is None:
            break
    return l3

# MongoDB connection
uri = "mongodb+srv://user:shakthi@cluster0.xfrul.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


c = pymongo.MongoClient(uri)
   

d = c["sam"]

# Getting all channel info
def get_info(id):
    channel_info=get_det(id)
    playlist_info=playlist_id(id)
    video=video_id(id)
    video_information=video_info(video)
    comment_info=get_comment_info(video)
    d=c["sam"]
    coll1=d["channel_details"]
    x={"channel_info":channel_info,"playlist_info":playlist_info,"video_info":video_information,"comment_info":comment_info}
    coll1.insert_one(x)
    return "upload completed "



# MySQL connection


# Creating channel table
# table for channels,playlist,videos,commentt.....
def channel_table(ch): 
    mydb = mysql.connector.connect(host="localhost", user="root", password="shakthi07", database="youtube1")
    cursor = mydb.cursor()
    try:   
        q='''create table if not exists channel(Channel_name varchar(50),Channel_id varchar(100) primary key,
                                Subscribers int,
                                views int,
                                Total_views int,
                                Channel_Description text,
                                playlist_id varchar(100))'''
        cursor.execute(q)
        mydb.commit()
    except:
        print("aldready created...")
    
    l=[]
    uri = "mongodb+srv://user:shakthi@cluster0.xfrul.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


    c = pymongo.MongoClient(uri)
    d = c["sam"]
    coll1=d["channel_details"]
    for i in coll1.find({"channel_info.channel_name":ch},{"_id":0}):
        l.append(i["channel_info"])
    df=pd.DataFrame(l)
    

    
    for index,row in df.iterrows():
        q='''insert into channel(Channel_name,Channel_id,Subscribers,views,Total_views,Channel_Description,
            playlist_id) values(%s,%s,%s,%s,%s,%s,%s)'''
    
        values = (row['channel_name'], row['id'], row['subscriber'], row['view_count'],
                  row['tot_video'], row['des'], row['playlist_id'])
        try:
            cursor.execute(q,values)
            mydb.commit()
        except:
            n=f"provided channel name{ch} already exists"
            return n
            
def playlist_table(ch):
    mydb = mysql.connector.connect(host="localhost", user="root", password="shakthi07", database="youtube1")
    cursor = mydb.cursor()
    try:   
        q='''create table if not exists playlist(Channel_name varchar(50),Channel_id varchar(100) ,
                                playlist_id varchar(100) primary key,
                                tittle varchar(50),
                                publish_date varchar(50))'''
        cursor.execute(q)
        mydb.commit()
    except:
        print("aldready created...")
    l=[]
    c = pymongo.MongoClient(uri)
    d = c["sam"]
    coll1=d["channel_details"]
    for i in coll1.find({"channel_info.channel_name":ch},{"_id":0}):
        l.append(i["playlist_info"])
    df=pd.DataFrame(l[0])


    for index,row in df.iterrows():
        q='''insert into playlist(Channel_name,Channel_id,playlist_id,tittle,publish_date)
            values(%s,%s,%s,%s,%s)'''
        
        values = (row['channel_name'], row['channel_id'], row["playlist_id"], row['tittle'],
                  row['publish_date'])
        try:
            cursor.execute(q,values)
            mydb.commit()
        except:
            print("aldready inserted.....")

# Creating video table
def video_table(ch):
    mydb = mysql.connector.connect(host="localhost", user="root", password="shakthi07", database="youtube1")
    cursor = mydb.cursor()
    try:
        q = '''CREATE TABLE IF NOT EXISTS video(
            Channel_name VARCHAR(50),
            Channel_id VARCHAR(100),
            Video_id VARCHAR(50) PRIMARY KEY,
            Tittle VARCHAR(100),
            Tag TEXT,
            Thumbnail VARCHAR(200),
            Des TEXT,
            Pub_date VARCHAR(75),
            Duration VARCHAR(75),
            Views BIGINT,
            likes BIGINT,
            Comments INT,
            Fav_count INT,
            Defination VARCHAR(25),
            Caption_status VARCHAR(50)
        )'''
        cursor.execute(q)
        mydb.commit()
    except:
        st.write("Video table already created")

    l=[]
    c = pymongo.MongoClient(uri)
    d = c["sam"]
    coll1=d["channel_details"]
    for i in coll1.find({"channel_info.channel_name":ch},{"_id":0}):
        l.append(i["video_info"])
    df2=pd.DataFrame(l[0])
   

    for index, row in df2.iterrows():
        q = '''INSERT INTO video(Channel_name, Channel_id, Video_id, Tittle, Tag, Thumbnail, Des,
                Pub_date, Duration, Views,likes, Comments, Fav_count, Defination, Caption_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'''
        values = (
            row['channel_name'], row['channel_id'], row['video_id'], row['tittle'], json.dumps(row['tag']),
            row['thumbnail'], row['des'], row['pub_date'], row['duration'], row['views'],row["likes"], row['comments'],
            row['fav'], row['defination'], row['caption_status']
        )
        try:
            cursor.execute(q, values)
            mydb.commit()
        except:
            st.write("Already inserted...")

# Creating comments table
def comments_table(ch):
    mydb = mysql.connector.connect(host="localhost", user="root", password="shakthi07", database="youtube1")
    cursor = mydb.cursor()
    try:
        q = '''CREATE TABLE IF NOT EXISTS comments(
            Comment_id VARCHAR(50) PRIMARY KEY,
            Video_id VARCHAR(50),
            Comment_text TEXT,
            Comment_author VARCHAR(50),
            Comment_date VARCHAR(75)
        )'''
        cursor.execute(q)
        mydb.commit()
    except:
        st.write("Comments table already created")

    l=[]
    c = pymongo.MongoClient(uri)
    d = c["sam"]
    coll1=d["channel_details"]
    for i in coll1.find({"channel_info.channel_name":ch},{"_id":0}):
        l.append(i["comment_info"])
    df=pd.DataFrame(l[0])
    


    for index, row in df.iterrows():
        q = '''INSERT INTO comments(Comment_id, Video_id, Comment_text, Comment_author, Comment_date)
                VALUES (%s, %s, %s, %s, %s)'''
        values = (row['Comment_id'], row['video_id'], row['comment_text'], row['comment_author'], row['comment_date'])
        try:
            cursor.execute(q, values)
            mydb.commit()
        except:
            st.write("Already inserted...")

# Migrating data to MySQL
def tables(ch):
    n=channel_table(ch)
    if n:
        return n
    
    playlist_table(ch)
    video_table(ch)
    comments_table(ch)
    return "All tables are created"

# Streamlit UI
st.title("YouTube Data Harvesting and Warehousing")
input = st.text_input("Enter the channel id")
if st.button("Get the data"):
    if input:
        out = get_info(input)
        st.success(out)


l6=[]
d=c["sam"]
coll1=d["channel_details"]
for i in coll1.find({},{"_id":0,"channel_info":1}):
    l6.append(i["channel_info"]["channel_name"])

op=st.selectbox("select the channel",l6)


if st.button("Migrate to SQL"):
    if input:
        t = tables(op)
        st.success(t)

# Displaying tables
st.subheader("Check SQL Data:")
op = st.selectbox("Select the table", ["Channels", "playlist", "videos", "comments"])

def show_ch():
    ch_list=[]
    db=c["sam"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_info":1}):
        ch_list.append(ch_data["channel_info"])
    df=st.dataframe(ch_list)

    return df


def show_playl():
    pl_list=[]
    db=c["sam"]
    coll1=db["channel_details"]
    for pl_data in coll1.find({},{"_id":0,"playlist_info":1}):
        for i in range(len(pl_data["playlist_info"])):
            pl_list.append(pl_data["playlist_info"][i])
    df1=st.dataframe(pl_list)
    return df1

def show_video():
    vi_list=[]
    db=c["sam"]
    coll1=db["channel_details"]
    for vi_data in coll1.find({},{"_id":0,"video_info":1}):
        for i in range(len(vi_data["video_info"])):
            vi_list.append(vi_data["video_info"][i])
    df2=st.dataframe(vi_list)
    return df2

def show_comm():
    com_list=[]
    db=c["sam"]
    coll1=db["channel_details"]
    for com_data in coll1.find({},{"_id":0,"comment_info":1}):
        for i in range(len(com_data["comment_info"])):
            com_list.append(com_data["comment_info"][i])
    df3=st.dataframe(com_list)

    return df3

if op == "Channels":
    show_ch()
elif op == "playlist":
    show_playl()
elif op == "videos":
    show_video()
elif op == "comments":
    show_comm()



mydb=mysql.connector.connect(host="localhost",user="root",password="shakthi07",database="youtube1")
cursor = mydb.cursor()
question=st.selectbox("Select your question",("1. All the videos and the channel name",
                                              "2. channels with most number of videos",
                                              "3. 10 most viewed videos",
                                              "4. comments in each videos",
                                              "5. Videos with higest likes",
                                              "6. likes of all videos",
                                              "7. views of each channel",
                                              "8. videos published in the year of 2022",
                                              "9. average duration of all videos in each channel",
                                              "10. videos with highest number of comments"))

if question=="1. All the videos and the channel name":
    query1='''select tittle as videos,channel_name as channelname from video'''
    cursor.execute(query1)
    t1=cursor.fetchall()
    df=pd.DataFrame(t1,columns=["video title","channel name"])
    st.write(df)

elif question=="2. channels with most number of videos":
    query2='''select Channel_name as channelname,Total_views as no_videos from channel 
                order by Total_views desc'''
    cursor.execute(query2)
    t2=cursor.fetchall()
    df2=pd.DataFrame(t2,columns=["channel name","No of videos"])
    st.write(df2)

elif question=="3. 10 most viewed videos":
    query3='''select views as views,channel_name as channelname,tittle as videotitle from video 
                where views is not null order by views desc limit 10'''
    cursor.execute(query3)
    t3=cursor.fetchall()
    df3=pd.DataFrame(t3,columns=["views","channel name","videotitle"])
    st.write(df3)

elif question=="4. comments in each videos":
    query4='''select comments as no_comments,tittle as videotitle from video where comments is not null'''
    cursor.execute(query4)
    t4=cursor.fetchall()
    df4=pd.DataFrame(t4,columns=["no of comments","videotitle"])
    st.write(df4)

elif question =="5. Videos with higest likes":
    query6 = '''SELECT tittle AS video_title, channel_name AS channel_name, likes AS total_likes
                FROM video
                WHERE likes IS NOT NULL
                ORDER BY likes DESC LIMIT 10'''
    cursor.execute(query6)
    t5 = cursor.fetchall()
    df6 = pd.DataFrame(t5, columns=["video title", "channel name", "total likes"])
    st.write(df6)

elif question == "6. likes of all videos":
    query6 = '''SELECT tittle AS video_title, likes AS total_likes
                FROM video
                WHERE likes IS NOT NULL'''
    cursor.execute(query6)
    t6 = cursor.fetchall()
    df6 = pd.DataFrame(t6, columns=["video title", "total likes"])
    st.write(df6)

elif question=="7. views of each channel":
    query7='''select Channel_name as channelname ,views as totalviews from channel'''
    cursor.execute(query7)
    
    t7=cursor.fetchall()
    df7=pd.DataFrame(t7,columns=["channel name","totalviews"])
    st.write(df7)

elif question=="8. videos published in the year of 2022":
    query8='''select tittle as video_title,pub_date as videorelease,channel_name as channelname from video
                where extract(year from pub_date)=2022'''
    cursor.execute(query8)
    
    t8=cursor.fetchall()
    df8=pd.DataFrame(t8,columns=["videotitle","published_date","channelname"])
    st.write(df8)

elif question=="9. average duration of all videos in each channel":
    query9='''select channel_name as channelname,AVG(duration) as averageduration from video group by channel_name'''
    cursor.execute(query9)
    
    t9=cursor.fetchall()
    df9=pd.DataFrame(t9,columns=["channelname","averageduration"])

    T9=[]
    for index,row in df9.iterrows():
        channel_title=row["channelname"]
        average_duration=row["averageduration"]
        average_duration_str=str(average_duration)
        T9.append(dict(channeltitle=channel_title,avgduration=average_duration_str))
    df1=pd.DataFrame(T9)
    st.write(df1)

elif question=="10. videos with highest number of comments":
    query10='''select tittle as videotitle, channel_name as channelname,comments as comments from video where comments is
                not null order by comments desc'''
    cursor.execute(query10)
    
    t10=cursor.fetchall()
    df10=pd.DataFrame(t10,columns=["video title","channel name","comments"])
    st.write(df10)
