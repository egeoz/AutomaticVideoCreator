#!/usr/bin/env python3
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap, subprocess, os, praw, re

# Modify this section according to your account
reddit = praw.Reddit(
    user_agent="USER_AGENT",
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    username="REDDIT_USERNAME",
    password="REDDIT_PASSWORD"
)

# List of subreddits to scan
subredditList=["nosleep","idontworkherelady","talesfromtechsupport"]

postTextList=[]
postTitleList=[]

postLog=[]

folder=""

def getSubmissions(subreddit):
    for submission in reddit.subreddit(subreddit).hot(limit=5):
        if submission not in postLog:
            if len(submission.selftext)>200:
                text=re.sub(r"http\S+", "", submission.selftext)
                text=text.replace("reddit"," ")
                text=text.replace("Reddit"," ")
                text=re.sub("[@#$%^*()[]/<>?\|`~_]", " ", text)
            
                postLog.append(submission)
                postTitleList.append(submission.title)
                postTextList.append(text)


def createAudio(text, i):
    try:
        o=gTTS(text)
        o.save(str(i) + "/tts.mp3")
    except:
        print("TTS Error")

def createCover(background, foreground, font, text, i):
    formattedText=textwrap.wrap(text, width=50)
    
    textFont=ImageFont.truetype(font,60)
    cover=Image.new("RGB", (1920,1080), color=background)
    
    coverDraw=ImageDraw.Draw(cover)
    
    current_h, pad=300, 10
    for line in formattedText:
        w, h=coverDraw.textsize(line, font=textFont)
        coverDraw.text(((1920 - w) / 2, current_h), line, font=textFont)
        current_h += h + pad
    
    cover.save(str(i) + "/cover.png")

def createVideo(i, sound, images):
    os.system("bash generate_video.sh " + str(i) + " " + sound + " " + images)

def init(i):
    try:
        os.mkdir(str(i))
    except:
        print("Cannot create video folder!")
        os.exit()
    
    with open(str(i) + "/file_list.txt", "w") as file_list: 
        file_list.write("file intro.mp4\n")
        file_list.write("file slideshow.mp4\n")

if __name__ == '__main__':
    getSubmissions(subredditList[0])
    for i in range(0,len(postTitleList)):
        init(i)
        createCover("black", "white", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", postTitleList[i], i)
        createAudio(postTextList[i], i)
        # Create a video using wind.mp3 as background music and use the images in images/horror/ for slideshow
        createVideo(i, "wind", "horror")
