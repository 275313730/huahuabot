from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.message import run_preprocessor

from ..handle import user


@run_preprocessor
async def check_ban(matcher: Matcher, event: PrivateMessageEvent):
    qq = event.user_id
    exist = user.check_qq_exist(qq)
    ban = user.check_qq_ban(qq)
    if not exist:
        await matcher.finish("加入树洞才能使用其他指令哦")
    if ban:
        await matcher.finish("账号封禁中，如有疑问可以通过'/反馈树洞'提交意见")
