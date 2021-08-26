import openai
import speech_recognition as sr
from gtts import gTTS
import os

# HUMAN GOES FIRST

openai.api_key=open('key.txt', 'r').read()


text = open('prompt.txt', 'r').read()

print(text)
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Human: ", end='')
        audio = r.listen(source)
    
    try:
        user_says = r.recognize_google(audio)
        text += 'Human: ' + user_says + '\n'

        if user_says == 'quit':
            quit()

        print(user_says)

        completion = openai.Completion.create(
            engine="davinci", 
            prompt=text, 
            stop=["Human:", "\n"],
            temperature=0.9,
            max_tokens=200)

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
    except sr.UnknownValueError: ...
    except sr.RequestError as e: print("Could not request results from Google Speech Recognition service; {0}".format(e))

    