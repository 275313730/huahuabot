import json
from bilireq.live import get_rooms_info_by_uids
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.log import logger

from ...database import db
from ...utils import safe_send, scheduler

status = {}


@scheduler.scheduled_job("interval", seconds=10, id="live_sched")
async def live_sched():
    """直播推送"""
    uids = db.get_uid_list()

    if not uids:  # 订阅为空
        return
    logger.debug(f"爬取直播列表，目前开播{sum(status.values())}人，总共{len(uids)}人")
    res = await get_rooms_info_by_uids(uids, reqtype="web")
    if not res:
        return
    for uid, info in res.items():
        new_status = 0 if info["live_status"] == 2 else info["live_status"]
        if uid not in status:
            status[uid] = new_status
            continue
        old_status = status[uid]
        if new_status == old_status:  # 直播间状态无变化
            continue
        status[uid] = new_status

        name = info["uname"]
        if new_status:  # 开播
            room_id = info["short_id"] if info["short_id"] else info["room_id"]
            url = "https://live.bilibili.com/" + str(room_id)
            title = info["title"]
            cover = (
                info["cover_from_user"] if info["cover_from_user"] else info["keyframe"]
            )
            logger.info(f"检测到开播：{name}（{uid}）")

            live_msg = (
                f"{name} 正在直播：\n{title}\n" +
                MessageSegment.image(cover) + f"\n{url}"
            )
        else:  # 下播
            logger.info(f"检测到下播：{name}（{uid}）")
            live_msg = f"{name} 下播了"

        push_list = db.get_sub_list(int(uid))
        for qq in push_list:
            await safe_send(
                bot_id=1778916839,
                send_type="private",
                type_id=qq,
                message=live_msg
            )
        db.update_user(int(uid), name)
