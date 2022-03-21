import asyncio
from operator import le
import traceback
from datetime import datetime, timedelta

from nonebot.log import logger

from bilireq.dynamic import get_user_dynamics
from ...database import db
from ...libs.dynamic import Dynamic
from ...utils import safe_send, scheduler, get_dynamic_screenshot

from ...database import db

last_time = {}


@scheduler.scheduled_job("interval", seconds=10, id="dynamic_sched")
async def dy_sched():
    """订阅推送"""

    uid = db.next_uid()
    if not uid:
        return
    up_name = db.get_up_name(uid)[0]

    logger.debug(f"爬取动态 {up_name}（{uid}）")
    dynamics = (await get_user_dynamics(uid)).get("cards", [])  # 获取最近十二条动态
    # config['uid'][uid]['name'] = dynamics[0]['desc']['user_profile']['info']['uname']
    # await update_config(config)

    if len(dynamics) == 0:  # 没有发过动态或者动态全删的直接结束
        return

    if uid not in last_time:  # 没有爬取过这位主播就把最新一条动态时间为 last_time
        dynamic = Dynamic(**dynamics[0])
        last_time[uid] = dynamic.time
        return

    for dynamic in dynamics[4::-1]:  # 从旧到新取最近5条动态
        dynamic = Dynamic(**dynamic)
        if (
            dynamic.time > last_time[uid]
            and dynamic.time
            > datetime.now().timestamp() - timedelta(minutes=10).seconds
        ):
            logger.info(f"检测到新动态（{dynamic.id}）：{up_name}（{uid}）")
            image = None
            for _ in range(3):
                try:
                    image = await get_dynamic_screenshot(dynamic.url)
                    break
                except Exception:
                    logger.error("截图失败，以下为错误日志:")
                    logger.error(traceback.format_exc())
                await asyncio.sleep(0.1)
            if not image:
                logger.error("已达到重试上限，将在下个轮询中重新尝试")
            await dynamic.format(image)

            data = db.get_sub_list(uid)
            if len(data) > 0:
                push_list = data[0]
                for qq in push_list:
                    await safe_send(1778916839, "private", qq, dynamic.message)

            last_time[uid] = dynamic.time
    await DB.update_user(uid, dynamic.name)  # type: ignore
