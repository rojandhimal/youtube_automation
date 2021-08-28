import os
import re
import random
import pytube
import urllib.request
import moviepy.editor as mp # pip install moviepy 

 
def removeDownloadFile(dir):
    print("start delete")
    for f in os.listdir(dir):
        print("deleting file",f)
        os.remove(os.path.join(dir, f))


dir = './videos'  #direcctory where you want to store or download videos
search_keyword = ["ncs", "nocopyrightsounds","ncsmusic","nocopyrightmusic","nocopyrightsound","royaltyfree" ]  #hastags to search video

def getYoutubeUrl(search_keyword):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + random.choice(search_keyword))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return video_ids


def downloadVideo(video_ids):
    yt = pytube.YouTube('https://www.youtube.com/watch?v='+ video_ids[0])
    yt.streams.filter(progressive=True,file_extension='mp4').order_by('resolution').desc().first().download(dir)


def convertVideo(dir):
    for f in os.listdir(dir):
        video=mp.VideoFileClip("videos/"+f)
        logo=(mp.ImageClip('logo.png')
                .set_duration(video.duration)
                .resize(height=100)
                .margin(right=290, top=20, opacity=0)
                .set_pos('right', 'top'))
        final=mp.CompositeVideoClip([video, logo])
        final.subclip(0).write_videofile("converted/"+ f)

video_ids = getYoutubeUrl(search_keyword)
downloadVideo(video_ids)
convertVideo(dir)
removeDownloadFile(dir)
removeDownloadFile("./converted")