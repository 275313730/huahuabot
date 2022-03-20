from nonebot import on_command
from nonebot.matcher import matchers
from nonebot.rule import to_me


help = on_command("help bilibili", aliases={
                  "help b站", "帮助 bilibili", "帮助 b站"}, rule=to_me(), priority=2, block=True)


@help.handle()
async def test():
    message = "b站小帮手目前支持的功能：\n（请将UID替换为需要操作的B站UID）"
    for matchers_list in matchers.values():
        for matcher in matchers_list:
            if (
                matcher.plugin_name
                and matcher.plugin_name.startswith("bilibili")
                and matcher.__doc__
            ):
                message += "\n"+matcher.__doc__
    message += (
        f""
    )
    await help.finish(message)
