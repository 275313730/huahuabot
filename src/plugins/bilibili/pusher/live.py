from nonebot.log import logger
from bilibili_api.user import User

from . import utils


status = {}


async def live(sub_list: list, uid: int):
    """直播推送"""

    # 获取直播间信息
    up_user = User(uid)
    res = await up_user.get_live_info()
    if not res:
        return
    name = res['name']
    live_room = res['live_room']
    new_status = live_room["liveStatus"]

    # 检查up是否已经轮询过
    if uid not in status:
        status[uid] = new_status
    old_status = status[uid]

    # 判断直播间状态是否有变化
    if new_status != old_status:
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

        # bot发送消息给订阅者
        for user_id in sub_list:
            await utils.safe_send(bot_id=1778916839, user_id=user_id, message=live_msg)

    status[uid] = new_status
