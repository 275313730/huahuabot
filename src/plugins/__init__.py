from xmlrpc.client import TRANSPORT_ERROR
from nonebot import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Bot, FriendRequestEvent
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import on_request


friend_req = on_request(priority=5)


@friend_req.handle()
async def friend_agree(bot: Bot, event: FriendRequestEvent):
    await bot.set_friend_add_request(flag=event.flag, approve=True)

bot_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@bot_help.handle()
async def _(event: PrivateMessageEvent):
    await bot_help.finish(f"这里是滑滑bot，目前已有的功能如下"
                          f"\n（'help'可替换为'帮助‘）"
                          f"\n树洞：/help 树洞"
                          f"\nb站小帮手：/help bilibili，/help b站"
                          f"\nbot反馈：/反馈"
                          f"\n注：bot每天凌晨4点会重启，请注意使用时避开重启时间，以免数据丢失")


feedback = on_command("反馈", rule=to_me(), priority=1, block=True)


@feedback.got("description", prompt="请输入反馈内容")
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    qq = event.user_id
    description = str(state['description'])

    await bot.send_private_msg(user_id=275313730, message=f"叮咚！有一个反馈来了"
                               f"\n反馈人qq：{qq}"
                               f"\n反馈内容：{description}")
    await feedback.finish("反馈成功")


update_push = on_command("更新提醒", rule=to_me(), priority=1, block=True)
