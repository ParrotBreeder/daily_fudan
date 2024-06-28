import random
import time
import sys
import requests
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


zlapp_login = 'https://uis.fudan.edu.cn/authserver/login?service=https://zlapp.fudan.edu.cn/site/ncov/fudanDaily'

def SendToDingDing(name):
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}' #钉钉token

    program = {
        "msgtype": "text",
        "text": {"content": f'{name}大蛤蟆今天没填'}
    }
    headers = {'Content-Type': 'application/json'}
    f = requests.post(webhook_url, data=json.dumps(program), headers=headers)
    print(f.text)


with open('./everyday_condition/{}{:0>2}{:0>2}.json'.format(time.localtime()[0], time.localtime()[1],
                                                            time.localtime()[2]), 'r',
          encoding='utf-8') as f:
    condition = json.load(f)

for i in condition:
    if not condition[i]:
        SendToDingDing(i)
        time.sleep(3)