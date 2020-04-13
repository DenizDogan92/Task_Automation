## Download youtube video files ##

from pytube import YouTube
import argparse, os
import urllib.request
from bs4 import BeautifulSoup

def how_to_use():
    scriptName = __file__.split("/")[-1]
    usage = "python %s" % (scriptName + " -v [VIDEO_NAME] [OPTIONS]\n\n"
                                 "OPTIONS:\n"
                                 "  -d, --musicDir" + " download directory\n"
                                 "  -a, --audioOnly" + " audio only flag (default=True)")
    return usage

def main():
    parser = argparse.ArgumentParser(description="youtube video downloader", usage=how_to_use())

    parser.add_argument("-v", "--videoName", nargs="*", help=argparse.SUPPRESS)
    parser.add_argument("-d" ,"--musicDir", default="./", help=argparse.SUPPRESS)
    parser.add_argument("-a", "--audioOnly", default=True, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if(args.videoName == None):
        print("usage: ", how_to_use())
        exit()

    videoName = " ".join(args.videoName)
    musicDir = args.musicDir
    audioOnly = True if str(args.audioOnly).lower() in ["t", "true", "y", "yes", "1"] else False

    ## send query to youtube and retrieve the top url's related to video name
    query = urllib.parse.quote(videoName)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    videoUrls = []
    for videoId, video in enumerate(soup.findAll(attrs={"class":"yt-uix-tile-link"})):
        videoUrl = "https://www.youtube.com" + video["href"]
        videoUrls.append(videoUrl)

        print("%d. %s" % (videoId+1, video["title"]))

    ## download the selected video names
    videoIds = list(map(int, input("\nEnter the video id(s) you like to download: ").split()))
    for videoId in videoIds:
        videoUrl = videoUrls[videoId-1]

        youtube = YouTube(videoUrl)
        videoTitle = youtube.title

        video = youtube.streams.filter(only_audio=audioOnly)
        video[0].download(musicDir)

        print("Video '%s' is downloaded" % (videoTitle))

    ## rename the video/audio files by replacing white spaces with "_"
    [os.rename(os.path.join(musicDir, f), os.path.join(musicDir, f).replace(" ", "_")) for f in os.listdir(musicDir)]

if(__name__ == "__main__"):
    main()