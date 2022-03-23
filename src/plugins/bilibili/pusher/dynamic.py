from datetime import datetime, timedelta
from nonebot.log import logger
from bilibili_api.user import User

from ..database import db

from . import utils


last_time = {}


async def dynamic(sub_list: list, uid: int):
    """动态推送"""

    # 获取动态信息
    up_user = User(uid)
    res = await up_user.get_dynamics()

    if not res:
        return

    dynamics = res['cards']

    if len(dynamics) == 0:  # 没有发过动态或者动态全删的直接结束
        return

    last_timestamp = dynamics[0]['desc']['timestamp']

    if uid not in last_time:  # 没有爬取过这位主播就把最新一条动态时间为 last_time
        last_time[uid] = last_timestamp
        return

    name = db.get_up_name(uid)[0][0]
    if (last_timestamp > last_time[uid]):
        dynamic_msg = str(f"{name}（{uid}）发布了新动态"
                          f"\nhttps://space.bilibili.com/{uid}/dynamic")

        # bot发送消息给订阅者
        for user_id in sub_list:
            await utils.safe_send(bot_id=1778916839, user_id=user_id, message=dynamic_msg)

    last_time[uid] = last_timestamp
    logger.debug(last_time)
