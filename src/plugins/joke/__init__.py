from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

from . import joke

get_joke = on_command("笑话", priority=2, block=True)


@get_joke.handle()
async def _():
    await get_joke.send(joke.get_a_joke("普通"))


get_hell_joke = on_command("地狱笑话", permission=SUPERUSER, priority=2, block=True)


@get_hell_joke.handle()
async def _():
    await get_joke.send(joke.get_a_joke("地狱"))


add_joke = on_command("添加笑话", permission=SUPERUSER, rule=to_me(), priority=1, block=True)


@add_joke.got("joke_type", prompt="请输入笑话类型（普通/地狱）")
@add_joke.got("joke_content", prompt="请输入笑话内容")
async def _(state: T_State):
    joke_type = str(state["joke_type"])
    joke_content = str(state["joke_content"])
    status = joke.add_joke(joke_type, joke_content)
    if status:
        await add_joke.send(f"添加成功，笑话如下"
                            f"\n笑话类型：{joke_type}"
                            f"\n笑话内容：{joke_content}")
    else:
        await  add_joke.send("添加失败，笑话可能存在")


check_jokes = on_command("查看笑话", permission=SUPERUSER, rule=to_me(), priority=1, block=True)


@check_jokes.handle()
async def _(event: Event):
    args = str(event.get_message()).split(" ")
    if len(args) > 1:
        part_of_jokes = joke.get_part_of_jokes(int(args[1]))
        if not part_of_jokes == "":
            await check_jokes.send(part_of_jokes)
        else:
            await check_jokes.send("页数错误")
