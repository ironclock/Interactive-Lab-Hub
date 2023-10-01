import requests  
import vlc
import yt_dlp
import json
from enum import Enum
from googleapiclient.discovery import build
import time
import helper
import threading

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

def callGPT(message, instruction_type, mood = "", emoji = ""):
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

def contains_tag(url):
    return "tag=244" in url

def playYoutubeVideo(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_duration = info['duration']

        formats = info['formats']
        audioUrl = ""
        videoUrl = ""
        for fmt in formats:
            url = fmt['url']
            if contains_tag(url):
                videoUrl = url
            # Here we're making an assumption that the 6th format is the audio. This may not always be true.
            if fmt['format_id'] == '140':  # Typically format '140' is m4a audio. Adjust if needed.
                audioUrl = url

        start_event = threading.Event()  # Synchronization event
        start_event.clear()  # Ensure event is cleared initially

        audio_thread = threading.Thread(target=helper.play_audio, args=(audioUrl, start_event))
        video_thread = threading.Thread(target=helper.play_video, args=(videoUrl, start_event))

        audio_thread.start()
        video_thread.start()

        # time.sleep(10)  # Allow the video thread to initialize
        # print("after 10 seconds")

        start_event.set()  # Signal both threads to start

        audio_thread.join()  # Wait for audio to finish
        video_thread.join()  # Wait for video to finish

        player = vlc.MediaPlayer(audioUrl)
        player.play()

        while player.get_state() != vlc.State.Ended:
            time.sleep(0.5)




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