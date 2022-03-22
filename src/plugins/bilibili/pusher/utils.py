import nonebot
from nonebot.log import logger


async def safe_send(bot_id: int, user_id: int, message: str):
    """发送出现错误时, 尝试重新发送, 并捕获异常且不会中断运行"""

    try:
        bot = nonebot.get_bots()[str(bot_id)]
    except KeyError:
        logger.error(f"推送失败，Bot（{bot_id}）未连接")
        return

    return await bot.call_api(api="send_msg", message=message, user_id=user_id)
