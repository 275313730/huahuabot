from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Bot
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

from ...config import TREE_HOLE_PRIORITY
from ..handle import user

ignore_cmds = ['/help', '/帮助', '/加入树洞']


@run_preprocessor
async def _(bot: Bot, matcher: Matcher, event: PrivateMessageEvent):
    # 只处理树洞相关matcher
    if matcher.priority and matcher.priority != TREE_HOLE_PRIORITY:
        return

    args = str(event.get_message())

    # 忽略prompt
    if not args.startswith("/"):
        return

    # 忽略help和加入树洞
    if args.startswith('/help') or args.startswith('/帮助') or args.startswith('/加入树洞'):
        return

    # 检查用户状态
    qq = event.user_id
    exist = user.check_qq_exist(qq)
    ban = user.check_qq_ban(qq)
    if not exist:
        await bot.send_private_msg(user_id=qq, message="请加入树洞后再使用其他指令哦")
        raise IgnoredException("reason")
    if ban:
        await bot.send_private_msg(user_id=qq, message="账号封禁中，如有疑问可以通过'/反馈'提交意见")
        raise IgnoredException("reason")

    user.update_last_use_time(qq)
