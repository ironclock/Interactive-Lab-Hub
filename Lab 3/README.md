# Chatterboxes

**COLLABORATORS:**

**Shai Aarons (sla88)**

**Ariana Bhigroog (ab2959)**

**Jon Caceres (jc3569)**

**Rachel Minkowitz (rhm256)**

**Amando Xu (ax45)**
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

**Please note:** connect the webcam/speaker/microphone while the pi is *off*. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Setup 

*DO NOT* forget to work on your virtual environment! 

Run the setup script
```chmod u+x setup.sh && sudo ./setup.sh  ```

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the directory is a folder called `speech-scripts` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/speech-scripts $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files `.sh` by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/speech-scripts $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech
```
You can test the commands by running
```
echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? 
Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*

The file for this is `speak_jon.sh` inside of `Lab 3`


---
Bonus:
[Piper](https://github.com/rhasspy/piper) is another fast neural based text to speech package for raspberry pi which can be installed easily through python with:
```
pip install piper-tts
```
and used from the command line. Running the command below the first time will download the model, concurrent runs will be faster. 
```
echo 'Welcome to the world of speech synthesis!' | piper \
  --model en_US-lessac-medium \
  --output_file welcome.wav
```
Check the file that was created by running `aplay welcome.wav`. Many more languages are supported and audio can be streamed dirctly to an audio output, rather than into an file by:

```
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  piper --model en_US-lessac-medium --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -
```
  
### Speech to Text

Next setup speech to text. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 
```
pip install vosk
pip install sounddevice
```

Test if vosk works by transcribing text:

```
vosk-transcriber -i recorded_mono.wav -o test.txt
```

You can use vosk with the microphone by running 
```
python test_microphone.py -m en
```

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

The file for this is located in `speech-scripts\ask_user.sh` -- it uses a modified version of `test_microphone.py`


### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```

From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

# Lab 3 Part 1

## Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device.

**Storyboard:**
![IMG_1663](./storyboard.png)

**Verplank Diagram:**
![IMG_1663](https://github.com/arianab68/Interactive-Lab-Hub/assets/70418227/03afddab-939d-4905-baca-f334898717c4)


\*\***Describe and document your process.**\*\*

![UML Sequence Diagram](https://github.com/arianab68/Interactive-Lab-Hub/assets/70418227/b4502328-1af8-49ba-afff-03d6ecfdf7df)

1. User expresses how they feel to Spotipi
    * "Ugh, SpotiPi I'm frustrated"
2. SpotiPi asks the user if they want to maintain or uplift their current mood
3. User responds to SpotiPi
    * SpotiPi sends the user's response to GPT API. This parses user responses and returns the mood.
4. SpotiPi responds by playing the user a track based on their mood.
    * User mood is sent to Spotify API and returns a song that best fits the user's mood.

## Acting out the dialogue

**Recording:**

https://drive.google.com/file/d/1CsTcaqhqGRCiWhEwGoUZI8e1PQzRb178/view?usp=drivesdk

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

**Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**

* The dialogue did not seem much different from what we imagined it to be when acted out. The flow of the interaction between the device and the user was smooth and in line with what we imagined it to be. However, one thing we noticed from our interaction was that there may be a potential issue if the user gives more than one input to SpotiPi. How would SpotiPi handle more complex speech against user interactions? For example, if a user says to SpotiPi "Ugh, I'm sad... wait no, actually I'm happy", would SpotiPi register the first or second input as the mood? Which one will SpotiPi choose to map back to a song.

## Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
3. Make a new storyboard, diagram and/or script based on these reflections.

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

# Documentation


![UML Sequence Diagram](new-diagram.jpg)

## Imports and Dependencies

* json: Used to read API keys from keys.json and to convert OpenAI responses into JSON objects for Python processing.
* vlc: Utilized for streaming audio content from YouTube.
* yt_dlp: Enables the download of YouTube videos for subsequent streaming via VLC.
* googleapiclient.discovery (from build): Interfaces with Google's API for YouTube video search functionality.
* cv2: Used to stream video content to display.
* requests: Facilitates communication with OpenAI's API.
* Enum: Defines Enum classes for structured data representation.

## How-To Guide/Instructions

**System Overview**

The system integrates the Vosk toolkit for offline speech recognition and utilizes OpenAI's GPT model to process and understand user input. The primary functionality involves interpreting user requests to either play specific songs or provide songs based on expressed moods. Google's YouTube API is used to query a song and play the audio back to the user while also playing the video on the display.

**Workflow**

1. User Interaction: The user communicates with the Raspberry Pi, indicating a mood or specifying a song.
2. Voice to Text using Vosk: Vosk converts the user's spoken words into textual data.
3. GPT Processing: The transcribed text is sent to OpenAI's GPT API along with guiding instructions. The expected output from GPT is a JSON object in response to the user's input.
4. Flow Determination:
  * Flow 1: If a song request is detected, GPT returns a JSON object with a flow_1 key. Nested within is another JSON object holding song_name and artist_name. This information is relayed to YouTube's API to fetch the appropriate song, which is then played back.
  * Flow 2: For mood-based inputs, GPT responds with a flow_2 key with the mood and an associated emoji as its value. The system subsequently inquires if the user intends to maintain or alter their mood. GPT then suggests a song that aligns with the mood, again providing song_name and artist_name. This is passed to the YouTube API, and the song is played.
  * Flow 3: We tell the user we could not understand if GPT could not properly parse their request. Then we loop back to the beginning of the program.

The program is designed to interpret user input and either provide the most relevant song based on the user's mood or directly play a song being requested.

[*Include videos or screencaptures of both the system and the controller.*](https://drive.google.com/file/d/1N2bTheywNG519HbHWdE2rQMpZ0_qjqzU/view?usp=sharing)

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

We opted to work with the ChatGPT API to parse the spoken words into instructions. We chose ChatGPT as we were able to prompt it to filter out exactly the content that we wanted to know - whether someone wanted to listen to a specific song, artist, genre, or whether they were in a mood/feeling or whether the input they told us wasnt relevant to playing music at all. ChatGPT also allows the user to speak the widest bredth of information and then Chatty does the insinuation for us to get a specific song from the Spotify API.  

Note: We used GPT-3.5 for the API but noticed that it was repeating songs and not being as creative as expected. We tested the spotipi out with GPT-4.0 which is taught on more diverse dataset and which's temperature can be adjusted (the creativity level of it's responses).

Shai: The user flows that we had defined for our system also worked really well in terms of limiting the scope of possibilities because of using GPT. This was done with clever prompt engineering and a significant amount of trial and error. The prompts we landed on provided us with mostly reliable feedback. 

The video display was also incredibly crisp in showing music videos for the device. This was a design choice, because YouTube's API allowed us to search for videos, whereas Spotify's API (what we originally intended to use), would not allow us to play songs. This landed up being a major win in our favor, having any music video available for use in our device. 

Amando: The system is able to discern mood based on what the user tells it regarding their day. Both users felt that it was kind of magical that the system was pretty spot on in how the user was feeling. However, with the second attempt of our first user, the device advised a song that was not very appropriate in maintaining the mood of the user. 
The video playback on the Pi was very cool as reported by both users. The screen showed the music video of the associated song that was playing and the audio synced up well with the video. One feedback we received from the users was that the screen was too small to pleasantly enjoy the music video while listening to the audio.

### What worked well about the controller and what didn't?

Shai: The controller worked significantly effectively at detecting and correctly transforming American male voice input. The controller struggled to recognize voices that had non-American accents. For some group members, it would take multiple attempts for the controller to identify what the group member was saying correctly, and this can cause inconvenience. Further, there was a slight delay in input vs. output of voice to text and visa versa. This was suitable for the context of this lab, however, in a commercial product, this may be less accepted. 

Amando: Using a speaker set up where the microphone is also housed within the same device worked well as it felt like the device was listening and talking back as a single unit. The microphone may not be the clearest at discerning each word that the user said, however the system was able to make up for this and provide a valid response. In the context of this lab, the microphone is adequate but in a more real-world application, it would be better to have a microphone with higher fidelity as feedback from one user. 

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

Shai: 
1) The Wizard of Oz interaction showed our group that voice and conversational-based devices are difficult to prototype. Humans all think in different ways, and conversations are incredibly unpredictable. We learned that it was impossible to count for every possible conversational input. We learned to bound/restrict conversational inputs into categories which helped dictate which flow should be enacted next in the device code.
2) The Wizard of Oz also showed us that it was important to provide users with feedback, especially if the user is using their voice for input. Without feedback, the user is unable to know if their voice input was captured correctly. We took these lessons and implemented the emoji system, where the user was presented with an emoji based on what the device captured as voice input. 

Amando: An ideal enhancement to the system would involve incorporating weather and temperature considerations, enabling it to determine if the user’s mood could be improved by addressing external atmospheric conditions that may adversely affect their mood. Subsequently, the system would proactively alert the user and suggest a suitable song for the circumstances.


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

Shai: We could use our system to build a database of a user's emotions throughout the day. This will allow for automatic song playing based on historical mood and emotional fluctuations depending on the time of day. Perhaps video and image could also be used as input here as facial expressions and body language are both clear indicators of emotional tone. Using video and images, as well as audio input, with historical data about emotions throughout the day, we can create an automated device that continually and automatically changes background songs depending on the mood given by the user.  

Amando: Besides recording down the moods of the user throughout the day, it could be made more long-term to track monthly fluctuations in mood as well as dealing with seasonal fluctuations of mood. With this dataset, we can make better recommendations with regards to time of the year. 
Other sensing modalities that would make sense to capture would be the user of the webcam itself on the controller. The webcam would be monitoring the user’s facial expression and when appropriate automatically suggest a song that could elevate the mood of the user. 

