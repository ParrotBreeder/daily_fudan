import json
import socket
import time

def Send_to_wechat(message):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9900))

    now_time = time.localtime()

    a = {'type':'dailyfudan',
         'name':'',
         'message':message}

    s.send(json.dumps(a).encode('utf-8'))
    s.close()

if_send = False
message = ''

with open('/home/ubuntu/daily_fudan/if_success.json', 'r') as f:
    data = f.read()

data = json.loads(data)

if data['time'] != '%d.%d.%d'%(time.localtime()[0], time.localtime()[1], time.localtime()[2]):
    if_send = True
    message += '时间异常，请检查'
else:
    for i in data.items():
        if not i[1]:
            if_send = True
            message += '{}的平安复旦异常。\n'.format(i[0])

if if_send:
    Send_to_wechat(message)
else:
    Send_to_wechat('All right!')
