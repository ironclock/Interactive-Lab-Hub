import requests  
import pafy
import vlc
import time
import yt_dlp
import pygame

def callGPT(message, firstInstructions = False, secondInstructions = False, mood = ""):

  instructions_one = "I'm going to be making a request of a song and it's going to yield one of two flows. It is up to you to decide which flow to take. Flow 1 would be one of the following: a request for a specific song, OR the name of an artist (you pick a song by the artist), OR a genre (you pick the song). Flow 2 would be an indication of my emotions and/or how I'm currently feeling. If you choose Flow 1, return to me the following: a dictionary containing the key `flow_1` with two values, one being song name, and the other being artist name. If you choose Flow 2, return a dictionary containing the key `flow_2`. I'm going to provide you six mood categories. You must categorize my mood within one of these six categories: ['happy', 'sad', 'fear', 'tired', 'anger', 'aroused']. Pick one of the categories and use it as the value for the key `flow_2`. If I am not making a request for a song or if I'm not making any kind of indication of how I'm feeling, return the key `flow_3`. Do not provide ANY other output besides a dictionary. The request will now follow: "

  instructions_two = "I'm going to tell you that I either want to feel different or I want to maintain my current mood. The mood I'm feeling is: " + mood + ". If I tell you that I want to feel different, then I want you to pick a RANDOM song that will change my mood. If I tell you that I want to maintain my current mood, then I want you to pick a RANDOM song that matches my mood. With this information and the choice I'm about to give you, ONLY return a dictionary containing the song name with `song_name` as the key and the artist name with `artist_name` as the key. DON'T PROVIDE ANYTHING ELSE. My choice is as follows: "

  instructions = ""

  if firstInstructions:
    instructions = instructions_one
  elif secondInstructions:
    instructions = instructions_two

  # Define the payload
  payload = {
      "model": "gpt-4.0-turbo",
      "messages": [
          {
              "role": "user",
              "content": instructions + message,
          }
      ],
      "max_tokens": 50,
      "temperature": 0,
      "top_p": 0,
      "n": 1,
      "stream": False
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

def playYoutubeVideo():
  URL = 'https://www.youtube.com/watch?v=oDBxIk2jYyo'

  ydl_opts = {}
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # get all information about the youtube video
      info = ydl.extract_info(URL, download=False)
      
      formats = info['formats']
      print(f"Found {len(formats)} formats")
      # iterate through all of the available formats
      for i,format in enumerate(formats):
          # print the url
          url = format['url']
          print(f"{i}) {url}")
          # each format has many other attributes. You can do print(format.keys()) to see all possibilities
      url = "https://rr2---sn-ab5sznzl.googlevideo.com/videoplayback?expire=1695807968&ei=gKUTZYTCHcOc_9EPzuKmgA8&ip=69.203.66.242&id=o-AGqWi3mKNpsirPnAaLR2KX3EEI0YJIuT2lxQ0Lb4gjpP&itag=139&source=youtube&requiressl=yes&mh=y5&mm=31%2C29&mn=sn-ab5sznzl%2Csn-ab5l6nrr&ms=au%2Crdu&mv=m&mvi=2&pl=17&initcwndbps=1672500&vprv=1&svpuc=1&mime=audio%2Fmp4&gir=yes&clen=1573892&dur=257.927&lmt=1570341205170835&mt=1695786068&fvip=1&keepalive=yes&fexp=24007246&beids=24350017&c=IOS&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Csvpuc%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAO_bJw-3Muu_5WohLaYrv3pNo6DpxDyvqDNbqZojHJfUAiEA6V4lRNTUmyrXJFjVxw2VGlF8ya85CqJ9dZZW2w6Pu2k%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgPQy6odp9aMJbkXPTsBJiXIO8XXlJx3lRuB71TWgUBzYCIQCDHkknXMLOinVT4U1IaUjQa3xRS_Meo5UdK4QStDftWQ%3D%3D"

      player = vlc.MediaPlayer(url)
      player.play()

def playYoutubeVideoTwo():
  URL = 'https://www.youtube.com/watch?v=oDBxIk2jYyo'

  ydl_opts = {}
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      # get all information about the youtube video
      info = ydl.extract_info(URL, download=False)
      
      formats = info['formats']
      print(f"Found {len(formats)} formats")
      # iterate through all of the available formats
      for i,format in enumerate(formats):
          # print the url
          url = format['url']
          print(f"{i}) {url}")
          # each format has many other attributes. You can do print(format.keys()) to see all possibilities
      url = "https://rr2---sn-ab5sznzl.googlevideo.com/videoplayback?expire=1695807968&ei=gKUTZYTCHcOc_9EPzuKmgA8&ip=69.203.66.242&id=o-AGqWi3mKNpsirPnAaLR2KX3EEI0YJIuT2lxQ0Lb4gjpP&itag=139&source=youtube&requiressl=yes&mh=y5&mm=31%2C29&mn=sn-ab5sznzl%2Csn-ab5l6nrr&ms=au%2Crdu&mv=m&mvi=2&pl=17&initcwndbps=1672500&vprv=1&svpuc=1&mime=audio%2Fmp4&gir=yes&clen=1573892&dur=257.927&lmt=1570341205170835&mt=1695786068&fvip=1&keepalive=yes&fexp=24007246&beids=24350017&c=IOS&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Csvpuc%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAO_bJw-3Muu_5WohLaYrv3pNo6DpxDyvqDNbqZojHJfUAiEA6V4lRNTUmyrXJFjVxw2VGlF8ya85CqJ9dZZW2w6Pu2k%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgPQy6odp9aMJbkXPTsBJiXIO8XXlJx3lRuB71TWgUBzYCIQCDHkknXMLOinVT4U1IaUjQa3xRS_Meo5UdK4QStDftWQ%3D%3D"
      
      temp_filename = "temp_audio_file.mp4"
      response = requests.get(url)
      with open(temp_filename, 'wb') as temp_file:
        print("downloading")
        temp_file.write(response.content)

      pygame.mixer.init()
      pygame.mixer.music.load(temp_filename)
      pygame.mixer.music.play()
      time.sleep(30)
      pygame.mixer.music.stop()


    # player = vlc.MediaPlayer(url)
    # player.play()