import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_c2c_message_create(self, message: C2CMessage):
        msg = message.content.strip()
        user_openid = message.author.user_openid
        #print(f"[Info] bot 收到消息：{member_openid}" + message.content)
        if msg == '记录私聊':
            if not os.path.exists("./c2c_id.json"):
                os.system(r'touch {}'.format('./c2c_id.json'))
            try:
                with open('./c2c_id.json','r',encoding="utf-8") as c2c_id:
                    c2c_id = json.load(c2c_id)
            except:
                c2c_id = {}
            c2c_id[user_openid] = message.id
            with open('./c2c_id.json','w',encoding="utf-8") as c2c:
                json.dump(c2c_id,c2c,ensure_ascii=False)
            messageResult = await message._api.post_c2c_message(
                openid=user_openid,
                msg_id=message.id,
                content=f"已记录私聊ID")
        if msg.startswith("/r"):
            result = dice.roll(msg, user_openid)
            messageResult = await message._api.post_c2c_message(
                openid=user_openid,
                msg_id=message.id,
                content=f"{result}")
    async def on_group_at_message_create(self, message: GroupMessage):
        msg = message.content.strip()
        member_openid = message.author.member_openid
        print("[Info] bot 收到消息：" + message.content)

        if msg == f"我喜欢你":
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"我也喜欢你")

        elif msg.startswith("/今日运势"):

            result = fortune_by_sqlite.get_today_fortune(member_openid)
            file_url = img_upload.get_upload_history()
            # print(result)
            messageResult = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,
                url=file_url
            )
            # 资源上传后，会得到Media，用于发送消息
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                msg_id=message.id,
                media=messageResult,
                content=f"{result}"
            )
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
    client.run(appid=test_config["appid"], secret=test_config["secret"])