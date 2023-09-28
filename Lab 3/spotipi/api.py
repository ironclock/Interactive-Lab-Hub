import requests  
import pafy
import vlc
import time
import yt_dlp
import pygame
from googleapiclient.discovery import build

def callGPT(message, firstInstructions = False, secondInstructions = False, mood = ""):

  # instructions_one = "I'm going to be making a request of a song and it's going to yield one of two flows. It is up to you to decide which flow to take. Flow 1 would be one of the following: a request for a specific song, OR the name of an artist (you pick a song by the artist), OR a genre (you pick the song). Flow 2 would be an indication of my emotions and/or how I'm currently feeling. If you choose Flow 1, return to me the following: a dictionary containing the key `flow_1` with two values, one being song name, and the other being artist name. If you choose Flow 2, return a dictionary containing the key `flow_2`. I'm going to provide you six mood categories. You must categorize my mood within one of these six categories: ['happy', 'sad', 'fear', 'tired', 'anger', 'aroused']. Pick one of the categories and use it as the value for the key `flow_2`. If I am not making a request for a song or if I'm not making any kind of indication of how I'm feeling, return the key `flow_3`. Do not provide ANY other output besides a dictionary. The request will now follow: "

  instructions_one = "I'm going to be making a request of a song and it's going to yield one of two flows. It is up to you to decide which flow to take. Flow 1 would be one of the following: a request for a specific song, OR the name of an artist (you pick a song by the artist), OR a genre (you pick the song). Flow 2 would be an indication of my emotions and/or how I'm currently feeling. If you choose Flow 1, return to me the following: a dictionary containing the key `flow_1` with two values, one being song name, and the other being artist name. If you choose Flow 2, return a dictionary containing the key `flow_2`. Make the mood I give you the value for the key `flow_2`. If I am not making a request for a song or if I'm not making any kind of indication of how I'm feeling, return the key `flow_3`. Do not provide ANY other output besides a dictionary. The request will now follow: "

  instructions_two = "I'm going to tell you that I either want to feel different or I want to maintain my current mood. The mood I'm feeling is: " + mood + ". If I tell you that I want to feel different, then I want you to pick a RANDOM song that will change my mood. I swear to god don't choose Happy by Pharrell Williams. If I tell you that I want to maintain my current mood, then I want you to pick a RANDOM song that matches my mood. With this information and the choice I'm about to give you, ONLY return a dictionary containing the song name with `song_name` as the key and the artist name with `artist_name` as the key. DON'T PROVIDE ANYTHING ELSE. My choice is as follows: "

  instructions = ""

  if firstInstructions:
    instructions = instructions_one
  elif secondInstructions:
    instructions = instructions_two

  # Define the payload
  payload = {
      "model": "gpt-4",
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

  headers = {
    "Authorization": "Bearer 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",  # Replace with your actual API key
    "Content-Type": "application/json"
  }

  # Send the POST request
  r = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
  response_data = r.json()
  content = response_data['choices'][0]['message']['content']

  return content

  # Print the response (optional)
  print(r.json())

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
    
API_KEY = 'AIzaSyArcJK_DAzm5Efjx1a8uw8u49LA97pHZVI'  # Replace with your API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

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