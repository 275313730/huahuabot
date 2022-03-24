from nonebot.log import logger
from bilibili_api.user import User

from . import utils


last_time = {}


async def dynamic(sub_list: list, uid: int, name: str):
    """动态推送"""

    # 获取动态信息
    up_user = User(uid)
    res = await up_user.get_dynamics()

    if not res:
        return

    dynamics = res['cards']

    if len(dynamics) == 0:  # 没有发过动态或者动态全删的直接结束
        return

    last_dynamic = dynamics[0]
    last_timestamp = last_dynamic['desc']['timestamp']

    if uid not in last_time:  # 没有爬取过这位主播就把最新一条动态时间为 last_time
        last_time[uid] = last_timestamp
        return

    if (last_timestamp > last_time[uid]):
        dynamic_url = last_dynamic['desc']['dynamic_id']

        dynamic_msg = str(f"{name}（{uid}）发布了新动态"
                          f"\n动态链接：https://t.bilibili.com/{dynamic_url}")

        # bot发送消息给订阅者
        for user_id in sub_list:
            await utils.safe_send(bot_id=1778916839, user_id=user_id, message=dynamic_msg)

    last_time[uid] = last_timestamp


def handle_dynamic_type(dynamic) -> str:
    dynamic_msg = ""

    dynamic_type = dynamic['desc']['type']
    card = dynamic['card']

    if dynamic_type == 4:
        content = card['content']
        dynamic_msg = str(f"\n动态类型：图文"
                          f"\n动态内容：{content}")

    if dynamic_type == 8:
        title = card['title']
        url = card['short_link']
        dynamic_msg = str(f"\n动态类型：视频"
                          f"\n动态标题：{title}"
                          f"\n视频链接：{url}")

    if dynamic_type == 2048:
        vest = card['vest']
        content = vest['content']
        sketch = card['sketch']
        live_title = sketch['title']
        live_content = sketch['desc_text']
        live_url = sketch['target_url']
        dynamic_msg = str(f"\n动态类型：live主题"
                          f"\n动态内容：{content}"
                          f"\nlive标题：{live_title}"
                          f"\nlive详情：{live_content}"
                          f"\nlive链接：{live_url}")

    return dynamic_msg
