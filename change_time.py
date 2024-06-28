import json
import os
import random
import re
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
time.sleep(5)

os.system('crontab -l > tmp.time')
with open('tmp.time', 'r') as f:
    data = f.read()

name = []
with open('message.txt', 'r', encoding='utf-8') as f:
    message = f.read()
message = message.split('\n')
message.pop(0)
for i in message:
    tmp = i.split(',')
    if tmp[0]:
        if tmp[0].startswith('#'):
            name.append(tmp[0][1:])
        else:
            name.append(tmp[0])

def EveryDayTime(x):
    result = []
    for i in name:
        for j in range(2):
            result.append(r'{} {} * * * python3 /home/ubuntu/daily_fudan/main.py -n {} > /home/ubuntu/daily_fudan/log/{}{:0>2}{:0>2}{}.log{} 2>&1'\
                          .format(random.randint(0, 59),
                                  random.randint(7, 10),
                                  i,
                                  time.localtime()[0],
                                  time.localtime()[1],
                                  time.localtime()[2],
                                  i, j))
    return x.group(1) + '\n'.join(result) + x.group(3)

data = re.sub(r'(####daily_fudan\n)([\s\S]*?)(\n####daily_fudan)', EveryDayTime, data)

with open('tmp.time', 'w') as f:
    f.write(data)

condition = {}
for i in name:
    condition[i] = False
condition = json.dumps(condition)
with open('./everyday_condition/{}{:0>2}{:0>2}.json'.format(time.localtime()[0], time.localtime()[1], time.localtime()[2]), 'w', encoding='utf-8') as f:
    f.write(condition)

os.system('crontab tmp.time')
os.system('rm tmp.time')



