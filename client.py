# -- coding: utf-8 --**
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, C2CMessage
from plugins import dice, pc_create,jrrp, pc_status
import re
import time
import json

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    #判断数据库初是否始化
    async def on_c2c_message_create(self, message: C2CMessage):
        msg = message.content.strip()
        member_openid = message.author.user_openid
        print(f"[Info] bot 收到消息：{member_openid}" + message.content)
        if msg == '记录私聊':
            if not os.path.exists("./c2c_id.json"):
                os.system(r'touch {}'.format('./c2c_id.json'))
            try:
                with open('./c2c_id.json','r',encoding="utf-8") as c2c_id:
                    c2c_id = json.load(c2c_id)
            except:
                c2c_id = {}
            c2c_id[member_openid] = message.id
            with open('./c2c_id.json','w',encoding="utf-8") as c2c:
                json.dump(c2c_id,c2c,ensure_ascii=False)
            messageResult = await message._api.post_c2c_message(
                openid=message.author.user_openid,
                msg_id=message.id,
                content=f"已记录私聊ID")
        if msg.startswith("/r"):
            result = dice.roll(msg, member_openid)
            messageResult = await message._api.post_c2c_message(
                openid=message.author.user_openid,
                msg_id=message.id,
                content=f"{result}")

    async def on_group_at_message_create(self, message: GroupMessage):
        msg = message.content.strip()
        member_openid = message.author.member_openid
        print("[Info] bot 收到消息：" + message.content)

        if msg.startswith("dr"):
            result = dice.dnd_roll(msg)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")
        elif msg.startswith("dc"):
            result = dice.dnd_check(msg)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")
        elif msg.startswith("r"):
            result = dice.roll(msg, member_openid)
            match = re.match(r'r(a)?([bp])?(\d+)?(h)?(.*)',msg)
            if match.group(4):
                try:
                    with open('./c2c_id.json','r',encoding="utf-8") as c2c_id:
                        c2c_id = json.load(c2c_id)
                except:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content=f"未记录私聊ID")
                user_c2c_id = c2c_id[member_openid]
                messageResult = await message._api.post_c2c_message(
                openid=member_openid,
                msg_id=user_c2c_id,
                content=f"{result}")
            else:
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"{result}")

        elif msg.startswith("/dnd") or msg.startswith("/DND"):
            result = pc_create.pcCreate(msg)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")

        elif msg.startswith("/coc") or msg.startswith("/COC"):
            result = pc_create.pcCreate(msg)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")

        elif msg == f"/jrrp" or msg == f".jrrp":
            result = jrrp.jrrp(member_openid)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")
            
        elif msg.startswith("st"):
            result = pc_status.st_main(msg, member_openid)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")

        elif msg.startswith("pc"):
            result = pc_status.pc_main(msg, member_openid)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")

        elif msg.startswith("sc"):
            result = pc_status.san_check(msg, member_openid)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")
        elif msg.startswith("en"):
            result = pc_status.en(msg, member_openid)
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"{result}")

        else:
            print("Normal")
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"收到：{msg}")

        _log.info(messageResult)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=config["appid"], secret=config["secret"])
