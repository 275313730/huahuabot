from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event

from . import activity

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _(event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) == 1:
        await _help.finish(f"这里是滑滑bot，以下为现有功能，输入/help xx即可获取相关功能指令"
                           f"\n/help 树洞"
                           f"\n/help 百闻牌"
                           f"\n/help 笑话"
                           f"\n/help 活动")
    else:
        if args[1] == "百闻牌录入":
            await _help.finish(f"百闻牌录入功能（必须私聊才可以使用）："
                               f"\n/已有式神：查看已录入式神"
                               f"\n/已有式神 xx：根据关键词筛选式神，目前可筛选范围有：性别，派系，系列（例如：/已有式神 红莲）"
                               f"\n/查看式神 xx：查看指定式神信息"
                               f"\n/添加式神"
                               f"\n/修改式神"
                               f"\n/添加卡牌"
                               f"\n/修改卡牌")
        elif args[1] == "百闻牌":
            await _help.finish(f"百闻牌相关指令："
                               f"\n/全部式神 or /所有式神：查看所有式神的名称"
                               f"\n/式神 xx：查看指定式神的卡牌（例如：/式神 不知火）"
                               f"\n/查看式神 xx：查看指定式神的文字描述")
        elif args[1] == "笑话":
            await _help.finish(f"笑话相关指令："
                               f"\n/笑话：获取一个随机笑话")
        elif args[1] == "活动":
            await _help.finish(f"活动相关指令："
                               f"\n/创建活动 日期 活动内容：创建新活动（例如：/创建活动 2月19日 水友赛，注意每次设置会重置活动信息）"
                               f"\n/参加活动 or /报名活动"
                               f"\n/退出活动"
                               f"\n/查看活动：查看活动信息和报名成员")
        elif args[1] == "树洞":
            await  _help.finish(f"树洞相关指令（只允许私聊使用）："
                                f"\n/加入树洞：必须先加入树洞，才可以使用其他指令"
                                f"\n/投递小纸条：根据指示投递小纸条到树洞中"
                                f"\n/捡个小纸条：随机获取一张别人投递的小纸条")


set_activity = on_command("创建活动", priority=3, block=True)


@set_activity.handle()
async def _(event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 2:
        activity.set_activity(args[1], args[2])
        await set_activity.send(f"新活动已创建，活动日期为{args[1]}，活动内容为{args[2]}")
    else:
        await set_activity.send("活动信息不完整，无法创建")


sign_up = on_command("参加活动", aliases={"报名活动"}, priority=3, block=True)


@sign_up.handle()
async def _():
    await sign_up.send(activity.sign_up())


get_activity_stats = on_command("查看活动", priority=3, block=True)


@get_activity_stats.handle()
async def _():
    await get_activity_stats.send(activity.get_activity_stats())
