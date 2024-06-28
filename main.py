import random
import time
import sys
import requests
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
import dailyfudan

zlapp_login = 'https://uis.fudan.edu.cn/authserver/login?service=https://zlapp.fudan.edu.cn/site/ncov/fudanDaily'

def SendToDingDing(name):
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}'  #钉钉token

    program = {
        "msgtype": "text",
        "text": {"content": f'{name}大蛤蟆又爆炸了'}
    }
    headers = {'Content-Type': 'application/json'}
    f = requests.post(webhook_url, data=json.dumps(program), headers=headers)
    print(f.text)


def run_fudan(name, uid, psw, sfzx, *args):
    daily_fudan = dailyfudan.Zlapp(uid, psw, url_login=zlapp_login)
    daily_fudan.login()
    if daily_fudan.check_change():
        daily_fudan.sfzx = int(sfzx)
        if not daily_fudan.check():
            daily_fudan.checkin()
        if daily_fudan.check():
            with open('./everyday_condition/{}{:0>2}{:0>2}.json'.format(time.localtime()[0], time.localtime()[1],
                                                                        time.localtime()[2]), 'r',
                      encoding='utf-8') as f:
                condition = json.load(f)
            condition[name] = True
            condition = json.dumps(condition)
            with open('./everyday_condition/{}{:0>2}{:0>2}.json'.format(time.localtime()[0], time.localtime()[1],
                                                                        time.localtime()[2]), 'w',
                      encoding='utf-8') as f:
                f.write(condition)
        daily_fudan.close()
    else:
        SendToDingDing(name)
        daily_fudan.close()
        sys.exit()

name = False
for i in sys.argv:
    if name:
        name = i
        break
    if i == '-n':
        name = True


with open('message.txt', 'r', encoding='utf-8') as f:
    message = f.read()
message = message.split('\n')
message.pop(0)
for i in message:
    if i:
        tmp = i.split(',')
        if tmp[0] == name:
            print(i)
            run_fudan(*tmp)
