#!/usr/bin/env python
# coding: utf-8
pip install fake-useragent

import requests
import json
import time
from datetime import date
from fake_useragent import UserAgent

telegram_chat_id = "@temperature_alert_alert"          
telegram_bot_id = "bot871626012:AAE_85JSqn8ns5RT5svfk7UUCqgMQL9wquM" 


DIST_ID =307
today = date.today()
format = "%d-%m-%Y"
today= today.strftime(format)
temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}
print(today)

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, today)
print(URL)


def send_telegram_message(message):
    url = "https://api.telegram.org/" + telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print("e")
        return False




while True:
    try:
        response = requests.get(URL,headers=browser_header)
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"]==45 and (session["available_capacity_dose1"]>0 or session["available_capacity_dose2"]>0 ):
                            name=center["name"]
                            ddate=session["date"]
                            dose1=session["available_capacity_dose1"]
                            dose2=session["available_capacity_dose2"]
                            vaccine=session["vaccine"]
                            print(name,ddate,dose1,dose2,vaccine)
                            message="ALERT\n Vaccine available\n{}\n{}\n{}\nDose1 {}\n Dose2 {}".format(name,vaccine,ddate,dose1,dose2)
                            send_telegram_message(message)
                            time.sleep(100)
                        else:
                            print("1")
