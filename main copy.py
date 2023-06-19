
import os
import telebot
import requests
import speech_recognition as sr
import subprocess
import datetime

from pydub import AudioSegment



logfile = str(datetime.date.today()) + '.log'
token = '5098007657:AAEwiPhBn7k-CR8q4FtPSYPJFNwrUEyGDxk'
bot = telebot.TeleBot(token)


import os
import soundfile as sf 

data, samplerate = sf.read('C:/Users/user/AppData/Local/Programs/Python/Python39/Scripts/JUP/file_49.ogg')
sf.write('C:/Users/user/Desktop/mstr_bot/fil.wav', data, samplerate)
os.system('C:/Users/user/Desktop/mstr_bot/fil.wav')

#process = subprocess.run(['ffmpeg', '-i', 'C:/Users/user/Desktop/mstr_bot/file_48.oga', 'sdsdsd'+'.wav'])
#given_audio = AudioSegment.from_file("C:/Users/user/AppData/Local/Programs/Python/Python39/Scripts/JUP/file_48.oga", format="oga")                                                
#given_audio.export("output_audio.wav", format="wav") 