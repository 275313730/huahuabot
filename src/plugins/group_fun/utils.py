import nonebot
from nonebot.log import logger


async def safe_send(bot_id: int, group_id: int, message: str):
    """发送出现错误时, 尝试重新发送, 并捕获异常且不会中断运行"""

    try:
        bot = nonebot.get_bots()[str(bot_id)]
    except KeyError:
        logger.error(f"推送失败，Bot（{bot_id}）未连接")
        return

    return await bot.call_api(api="send_msg", message=message, group_id=group_id)


def next_uid(uid_list: list, index: int) -> int:
    if len(uid_list) == 0:
        return -1
    return uid_list[index][0]
