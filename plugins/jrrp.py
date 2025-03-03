# -- coding: utf-8 --**
import os
import random
import time
from datetime import datetime, timedelta, timezone
import json

def get_china_time():
    SHA_TZ = timezone(timedelta(hours=8), name='Asia/Shanghai')
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)
    return(beijing_now.strftime('%Y-%m-%d'))

def jrrp(member_openid):
    rp_data = {}
    if not os.path.exists("./rp.json"):
        os.system(r'touch {}'.format('./rp.json'))
    with open('./rp.json','r',encoding="utf-8") as rp_dat:
        dic = rp_dat.read()
        if not dic == '':
            rp_data = json.loads(dic)
        rp_dat.close()
    with open('./rp.json','w',encoding="utf-8") as rp_dat:
        today = get_china_time()
        print(today)
        if not member_openid in rp_data:
            rp_data[member_openid] = {"rp":"", "date":"test"}
        if rp_data[member_openid]["date"] != today:
            rp = random.randint(1,100)
            rpz = (100-rp)/100
            if rpz >= 0.95:
                rpz = '爆棚'
                end = 'POP来打劫你的运气了！'
            elif rpz >= 0.75:
                rpz = '不错'
                end = 'POP都有点羡慕了，'
            elif rpz >= 0.6:
                rpz = '还行'
                end = '今天起码是走运的一天~'
            elif rpz >= 0.4:
                rpz = '一般般'
                end = '嘛~嘛，'
            elif rpz >= 0.25:
                rpz = '有点差'
                end = '出门记得看黄历'
            elif rpz >= 0.1:
                rpz = '不忍直视'
                end = '建议不要出门'
            else:
                rpz = '也太差了吧？'
                end = '哇！同我扯啊！别靠过来传染我！'
            rp_data[member_openid]["date"] = today
            result = f'你今天的人品{rpz}（{rp}）{end}'
            rp_data[member_openid]["rp"] = result
        else:
            result = f'你已经测过人品了，{rp_data[member_openid]["rp"]}'
        rp_data = json.dump(rp_data,rp_dat,ensure_ascii=False)
        rp_dat.close()
    return(result)