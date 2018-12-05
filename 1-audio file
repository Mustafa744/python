import speech_recognition as sr
r = sr.Recognizer()
harvard = sr.AudioFile('C:\harvard.wav')#file
with harvard as source:
    audio = r.record(source)

type(audio)

r.recognize_google(audio)
