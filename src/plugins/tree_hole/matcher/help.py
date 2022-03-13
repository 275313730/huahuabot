from nonebot import on_command

_help = on_command("help", aliases={"帮助"}, priority=1, block=True)


@_help.handle()
async def _():
    await _help.finish(f"这里是树洞bot，目前可以使用的功能有（只有私聊才有效）："
                       f"\n/加入树洞：必须先加入树洞，才可以使用其他指令哦"
                       f"\n/投递小纸条：根据指示投递小纸条到树洞中"
                       f"\n/捡个小纸条：随机捡取一张别人投递的小纸条"
                       f"\n/我的小纸条：查看自己投递过的小纸条"
                       f"\n/删除小纸条：删除一条自己投递过的小纸条"
                       f"\n/举报小纸条：遇到违反规则的小纸条请及时举报哦（请不要恶意举报）")
