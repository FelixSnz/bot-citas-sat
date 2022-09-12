import speech_recognition as sr
from pydub import AudioSegment
import requests


def mp3_to_wav(src_mp3_file):

    dst = "resources/temp.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src_mp3_file)
    sound.export(dst, format="wav")
    return dst

def download_mp3_url(mp3_url):
        doc = requests.get(mp3_url)
        mp3_file_savename = '../resources/temp.mp3'
        with open(mp3_file_savename, 'wb') as f:
            f.write(doc.content)
        return mp3_file_savename


def audio_file_to_text(audio_file_path:str):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text


