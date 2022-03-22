import json
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.log import logger
from bilibili_api.user import User

from . import utils
from ..database import db

from apscheduler.schedulers.asyncio import AsyncIOScheduler


status = {}

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job("interval", seconds=10, id="live_sched")
async def job():
    """直播推送"""
    uid = db.next_uid()

    if uid == -1:  # 订阅为空
        return

    logger.debug(f"爬取直播列表，目前爬取uid:{uid}")

    up_user = User(uid)
    res = await up_user.get_live_info()

    if not res:
        return

    name = res['name']
    live_room = res['live_room']

    new_status = live_room["liveStatus"]
    if uid not in status:
        status[uid] = new_status
    old_status = status[uid]
    if new_status != old_status:  # 直播间状态有变化
        if new_status == 1:  # 开播
            room_id = live_room["roomid"]
            url = "https://live.bilibili.com/" + str(room_id)
            title = live_room["title"]
            logger.info(f"检测到开播：{name}（{uid}）")

            live_msg = (
                f"{name} 正在直播：\n{title}\n" + f"\n{url}"
            )
        else:  # 下播
            logger.info(f"检测到下播：{name}（{uid}）")
            live_msg = f"{name} 下播了"

        sub_list_str = db.get_sub_list(int(uid))[0][0]
        sub_list = json.loads(sub_list_str)
        if len(sub_list) == 0:
            db.delete_up(uid)
        else:
            for user_id in sub_list:
                await utils.safe_send(bot_id=1778916839, user_id=user_id, message=live_msg)

    db.update_user(int(uid), name)
    status[uid] = new_status

scheduler.start()
