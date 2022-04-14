from random import randint
from ...config import GROUP_PRIORITY
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.typing import T_State
from nonebot import require
from .. import utils

scheduler = require("nonebot_plugin_apscheduler").scheduler
assert scheduler is not None
scheduler = scheduler.scheduler

games = []

prepare_words = ['聚气！', '凝神！', '残心！', '蓄力！', '目视！']


@scheduler.scheduled_job("interval", seconds=1, id="count_time")
async def count_time():
    global games
    for game in games:
        if game['status'] == 0:
            continue
        if game['status'] < 4:
            utils.safe_send(bot_id=1778916839,
                            user_id=game['group_id'], message=4-game['status'])
            game['status'] += 1
        elif game['status'] < 7:
            word = prepare_words[randint(0, 4)]
            utils.safe_send(bot_id=1778916839,
                            user_id=game['group_id'], message=word)
            random_num = randint(1, 10)
            if random_num > 7:
                game['status'] = 7
            else:
                game['status'] += 1
        else:
            utils.safe_send(bot_id=1778916839,
                            user_id=game['group_id'], message="拔刀！")
            games.remove(game)


create_game = on_command("居合斩", priority=GROUP_PRIORITY, block=True)


@create_game.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id
    creator_id = event.user_id

    global games

    for game in games:
        if game['group_id'] == group_id:
            create_game.finish("挑战已存在，请先完成当前挑战")

    games.append({"status": 0, "group_id": group_id, "players": [creator_id]})
    create_game.finish("挑战发起成功，请其他玩家输入'接受挑战'以继续")


join_game = on_command("接受挑战", priority=GROUP_PRIORITY, block=True)


@join_game.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id
    player_id = event.user_id
    game_create = False

    global games

    for game in games:
        if game['group_id'] == group_id:
            game_create = True

        if game_create:
            game['players'].append(player_id)
            join_game.send("加入成功，挑战即将开始，请双方做好准备")
            game['status'] = 1
            join_game.finish("在看到'拔刀！'的字样后，立即打出'斩'字，即可赢得胜利，提前拔刀将会视为失败")
        else:
            join_game.finish("挑战不存在，请先发起挑战")


cut = on_command("斩", priority=GROUP_PRIORITY, block=True)


@cut.handle()
async def _(event: GroupMessageEvent):
    group_id = event.group_id
    player_id = event.user_id
    game_create = False

    global games
    for game in games:
        if game['group_id'] == group_id:
            game_create = True

        if game_create:
            if player_id in game['players']:
                game['players'].remove(player_id)
                another_player_id = game['players'][0]
                games.remove(game)
                if game['status'] == 7:
                    cut.finish(
                        f"{player_id}快速拔刀击败了对方！\n胜利者是{another_player_id}！")
                else:
                    cut.finish(f"{player_id}提前拔刀！\n胜利者是{another_player_id}！")
