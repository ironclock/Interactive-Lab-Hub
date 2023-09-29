import requests  
import pafy
import vlc
import time
import yt_dlp
import pygame
import json
from enum import Enum
from googleapiclient.discovery import build

with open("keys.json", "r") as file:
    keys = json.load(file)

with open('instructions.json', 'r') as file:
    INSTRUCTIONS = json.load(file)

OPENAI_API_KEY = keys["OPENAI_API_KEY"]
YOUTUBE_API_KEY = keys["YOUTUBE_API_KEY"]

BASE_URL = 'https://api.openai.com/v1/chat/completions'

class Model(Enum):
   GPT4JUNE2023 = "gpt-4-0613"
   GPT4 = "gpt-4"
   GPT35TURBO = "gpt-3.5-turbo"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

def callGPT(message, instruction_type, mood = ""):
  instructions = INSTRUCTIONS[instruction_type].format(mood = mood)

  # Define the payload
  payload = {
      "model": Model.GPT4JUNE2023.value,
      "messages": [
          {
              "role": "user",
              "content": instructions + message,
          }
      ],
      "max_tokens": 256,
      "temperature": 1.5,
      "top_p": 1,
      "frequency_penalty": 0,
      "presence_penalty": 0
  }

  # Send the POST request
  r = requests.post('https://api.openai.com/v1/chat/completions', json = payload, headers = HEADERS)
  response_data = r.json()
  content = response_data['choices'][0]['message']['content']

  return content

def playYoutubeVideo(url):
  URL = url

  ydl_opts = {}
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # get all information about the youtube video
      info = ydl.extract_info(URL, download=False)
      
      formats = info['formats']
      print(f"Found {len(formats)} formats")
      # iterate through all of the available formats
      playUrl = ""
      for i,format in enumerate(formats):
          # print the url
          url = format['url']
          # print(f"{i}) {url}")
          if i == 5:
             playUrl = url
          # each format has many other attributes. You can do print(format.keys()) to see all possibilities
      # url = "https://rr1---sn-ab5l6nrr.googlevideo.com/videoplayback?expire=1695883057&ei=0coUZYmcL6yA_9EPp_uEgAc&ip=69.203.66.242&id=o-AII5g4QE1sIIeVMxkdp_pL4RbX0gSkbc6oTdz_HoWmFK&itag=139&source=youtube&requiressl=yes&mh=y5&mm=31%2C26&mn=sn-ab5l6nrr%2Csn-p5qddn7d&ms=au%2Conr&mv=m&mvi=1&pl=17&initcwndbps=1370000&vprv=1&svpuc=1&mime=audio%2Fmp4&gir=yes&clen=1573892&dur=257.927&lmt=1570341205170835&mt=1695860950&fvip=2&keepalive=yes&fexp=24007246&beids=24472436&c=IOS&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Csvpuc%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AGM4YrMwRAIgKZyoEoQOpMLFu86BMyn1FrEaEZ-fWnKBneAFjmfLOdICIFtqVERqCFXqBy2I4iPTJmqcDf7VrdnW2kLcSy4CAhBO&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AK1ks_kwRQIhAKTowinLoF17UoXtNkhgy4nWWj9VCbmiZfc1tD9Yd80qAiAmRMvtyPGlxWQTOUXEaHWSD7FA9npwYaA5dN01lA-VCQ%3D%3D"

      player = vlc.MediaPlayer(playUrl)
      player.play()

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = YOUTUBE_API_KEY)

def search_youtube(query, max_results=10):
    search_response = youtube.search().list(
        q=query,
        type="video",  # We're looking for videos (not channels or playlists)
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videoId = search_response['items'][0]['id']['videoId']
    return 'https://www.youtube.com/watch?v=' + videoId
    # videos = []

    # for search_result in search_response.get("items", []):
    #     title = search_result["snippet"]["title"]
    #     video_id = search_result["id"]["videoId"]
    #     videos.append((title, video_id))

    # return videos

# results = search_youtube("Python tutorial")
# for title, video_id in results:
#     print(title, f"https://www.youtube.com/watch?v={video_id}")