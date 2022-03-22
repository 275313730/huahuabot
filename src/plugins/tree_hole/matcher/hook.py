<<<<<<< HEAD
from nonebot.internal.matcher import Matcher, matchers
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.message import run_preprocessor
=======
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.message import run_preprocessor
from nonebot.matcher import matchers
>>>>>>> d2a5994fd68b6daf811e09f5962fb772e155d4ea

from ..handle import user

ignore_cmds = ['/help', '/帮助', '/加入树洞']


@run_preprocessor
async def _(matcher: Matcher, event: PrivateMessageEvent):
    # 识别树洞matcher
    if matcher.plugin_name and not matcher.plugin_name.startswith("tree_hole"):
        return

    # 忽略特殊指令
    args = str(event.get_message()).split(" ")
    if args[0] in ignore_cmds:
        return

    # 检查用户状态
    qq = event.user_id
    exist = user.check_qq_exist(qq)
    ban = user.check_qq_ban(qq)
<<<<<<< HEAD

=======
    if(matcher.plugin_name and not matcher.plugin_name.startswith("tree_hole")):
        return
>>>>>>> d2a5994fd68b6daf811e09f5962fb772e155d4ea
    if not exist:
        await matcher.finish("加入树洞才能使用其他指令哦")
    if ban:
        await matcher.finish("账号封禁中，如有疑问可以通过'/反馈树洞'提交意见")
    user.update_last_use_time(qq)
