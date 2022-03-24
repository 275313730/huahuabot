from nonebot import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Bot
from nonebot.rule import to_me
from nonebot.typing import T_State


_help = on_command("help", aliases={"帮助"}, priority=2, block=True)


@_help.handle()
async def _(event: PrivateMessageEvent):
    await _help.finish(f"这里是滑滑bot，目前已有的功能如下"
                       f"\n（'help'可替换为'帮助‘）"
                       f"\n树洞：/help 树洞"
                       f"\nb站小帮手：/help bilibli，/help b站"
                       f"\nbot反馈：/反馈"
                       f"\n注：bot每天凌晨4点会重启，请注意使用时避开重启时间，以免数据丢失")


feedback = on_command("反馈", rule=to_me(), priority=2, block=True)


@feedback.got("description", prompt="请输入反馈内容")
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    qq = event.user_id
    description = str(state['description'])

    await bot.send_private_msg(user_id=275313730, message=f"叮咚！有一个反馈来了"
                               f"\n反馈人qq：{qq}"
                               f"\n反馈内容：{description}")
    await feedback.finish("反馈成功")
