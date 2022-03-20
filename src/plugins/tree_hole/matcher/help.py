from nonebot import on_command

_help = on_command("help 树洞", aliases={"帮助 树洞"}, priority=1, block=True)


@_help.handle()
async def _():
    await _help.finish(f"树洞目前可以使用的功能有"
                       f"（请将UID改为小纸条编号）"
                       f"\n个人相关："
                       f"\n/加入树洞（必须先加入树洞，才可以使用其他指令哦）"
                       f"\n/修改昵称"
                       f"\n/我的小纸条"
                       f"\n/删除小纸条"
                       f"\n"
                       f"\n小纸条的投递与捡取："
                       f"\n/投递小纸条"
                       f"\n/捡取小纸条（已经捡取过的小纸条不会再重复捡取）"
                       f"\n"
                       f"\n小纸条收藏："
                       f"\n/收藏小纸条 UID"
                       f"\n/取消收藏小纸条 UID"
                       f"\n/我的收藏"
                       f"\n"
                       f"\n其他："
                       f"\n/举报小纸条（请不要恶意举报）"
                       f"\n"
                       f"\n注：1.以上功能只有私聊才有效"
                       f"\n2.为了方便操作，所有指令中的'小纸条'可以省略不输入")
