from nonebot.log import logger
from nonebot import require

from .live import live
from .dynamic import dynamic

from . import utils
from ..database import db

scheduler = require("nonebot_plugin_apscheduler")
assert scheduler is not None
scheduler = scheduler.scheduler


status = {}

uid_list: list = []
index = 0


def update_uid_list():
    global uid_list
    uid_list = db.get_uid_list()


@scheduler.scheduled_job("interval", seconds=5, id="pusher_sched")
async def pusher_sched():
    """推送"""

    global uid_list, index

    # 判断索引是否达到最大值
    if index + 1 >= len(uid_list):
        index = 0
        update_uid_list()
    else:
        index += 1

    # 获取uid
    uid = utils.next_uid(uid_list, index)

    # 判断订阅是否为空
    if uid == -1:
        return

    # 获取UP的信息
    name = db.get_up_name(uid)
    sub_list = db.get_sub_list(uid)

    # 自动删除无人关注的UP
    if sub_list is not None and len(sub_list) == 0:
        db.delete_up(uid)
        logger.info(f"UID:{uid}已无人关注，自动删除")
        return

    await live(sub_list, uid)
    await dynamic(sub_list, uid, name)
