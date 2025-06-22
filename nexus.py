import time 
import sys 
import os 
from colorama import Fore 
import pyttsx3 
from playsound import playsound
count=0
#getting the mp3 files from the os.listdir() function
mp3_files=[]
def loop_over(sequence,color,text_speed):
    for txt in sequence:
        sys.stdout.flush()
        time.sleep(text_speed)
        sys.stdout.write(f'{color}{txt}')
    else:
        print(Fore.RESET)
        
for file in os.listdir():
    #Checking if the extension of a file is mp3 or not 
    if file.endswith('.mp3')==True:
        mp3_files.append(file)
    else:
        continue 
else:
    loop_over(sequence='mp3 files:\n\t',color=Fore.CYAN,text_speed=0.1)
    for n in mp3_files:
        count+=1
        print(f'{Fore.GREEN}{count}. {n}')
        time.sleep(0.1)
    else:
     print(Fore.RESET)
     time.sleep(1)
    enter_file_alias=input('Enter the mp3 file you want to play:')
    while enter_file_alias not in mp3_files:
        if enter_file_alias not in mp3_files:
            time.sleep(1)
            loop_over(sequence=f'Error, the file you have just entered is not present in the mp3 list please try again.',color=Fore.RED,text_speed=0.1)
            time.sleep(1)
            enter_file_alias=input('Enter the mp3 file you want to play:')
    if enter_file_alias in mp3_files:
        time.sleep(1)
        try:
            time.sleep(1)
            integer=int(input('How many times do you want to play this mp3 file?:'))
            number_of_times_song_is_played=1
            for n in range(integer):
                strn=str(number_of_times_song_is_played)
                if strn.endswith('1'):
                    pyttsx3.speak(f'{enter_file_alias} playing for the {strn}st time')
                    time.sleep(1)
                    playsound(f'{enter_file_alias}')
                    number_of_times_song_is_played+=1
                elif strn.endswith('2'):
                    pyttsx3.speak(f'{enter_file_alias} playing for the {strn}nd time')
                    time.sleep(1)
                    playsound(f'{enter_file_alias}')
                    number_of_times_song_is_played+=1
                elif strn.endswith('3'):
                    pyttsx3.speak(f'{enter_file_alias} playing for the {strn}rd time')
                    time.sleep(1)
                    playsound(f'{enter_file_alias}')
                    number_of_times_song_is_played+=1
                else:
                    pyttsx3.speak(f'{enter_file_alias} playing for the {strn}th time')
                    time.sleep(1)
                    playsound(f'{enter_file_alias}')
                    number_of_times_song_is_played+=1
            else:
                time.sleep(1)
                pyttsx3.speak(f'{enter_file_alias} was played for the last time')
        except ValueError:
            loop_over(sequence='The program encountered a ValueError, please try again..',color=Fore.RED,text_speed=0.1)