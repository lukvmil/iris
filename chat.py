import openai
import speech_recognition as sr
from gtts import gTTS
import os
import pyaudio
import wave

import google.cloud.texttospeech as tts

def text_to_wav(text, voice_name='en-AU-Wavenet-A'):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(f'temp.wav', 'wb') as out:
        out.write(response.audio_content)
        print('done')

    chunk = 1024
    f = wave.open('temp.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()  

    
# HUMAN GOES FIRST

openai.api_key=open('key.txt', 'r').read()


text = open('prompt.txt', 'r').read()

counter = 0

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

        if not user_says and counter > 3:
            user_says = "1 day has passed."
            text += user_says + '\n'

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

        if resp:
            text_to_wav(resp[4:])

        with open('record.txt', 'w') as f:
            f.write(text)
    except sr.UnknownValueError: ...
    except sr.RequestError as e: print("Could not request results from Google Speech Recognition service; {0}".format(e))

    