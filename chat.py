import openai
import speech_recognition as sr
from gtts import gTTS
import os

# HUMAN GOES FIRST

openai.api_key=open('key.txt', 'r').read()


text = """
I am a hitchhiking robot named Iris that relies on human's goodwill to move around. I live on the campus of the University of Notre Dame and like talking to students. I often ask people to take me to new places.

Human: What is this thing?
AI: Hello! I am Iris, a hitchhiking robot. 
Human: What does that mean?
AI: It means I want you to carry me around to see new places and meet new people!
"""

print(text)
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        user_says = r.recognize_google(audio)
        text += 'Human: ' + user_says + '\n'

        completion = openai.Completion.create(
            engine="davinci", 
            prompt=text, 
            stop=["Human:", "\n"],
            temperature=0.9)

        resp = completion.choices[0].text
        print(resp)
        text += resp + '\n'


        file = "file.mp3"
        if resp:
            tts = gTTS(resp[4:])
        tts.save(file)

        os.system("play.bat")


        with open('record.txt', 'w') as f:
            f.write(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    