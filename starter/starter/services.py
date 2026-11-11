# -*- coding:utf-8 -*-
"""
次元语音伙伴 · 第1课：登记三位伙伴。
characters.py 里写好 Character 以后，在这个文件里用它造出三位伙伴，放进 ROLES。
页面按 ROLES 找伙伴：左边有几张卡片、点的是哪一位、跟谁聊天，都从这里取。
get_role、respond、speak 已经写好，不要改。
"""
from iflytek_kit import tts_say
from characters import Character


# --- 请完成 ---
# TODO[第1课-基础] ROLES：三位伙伴
#
# 页面上：左边的三张卡片。点哪一张，就由那一位打招呼、陪你聊天。
#
# 要做的事：
#     在下面的花括号里写三项。键照下面写，页面用这三个词认伙伴；值是用 Character(名字, 声线, 口癖) 造出来的一位伙伴：
#         "tsundere"   傲娇酱   声线 "x4_yezi"       口癖 "哼，才不是特意来陪你呢！"
#         "genki"      元气酱   声线 "x4_xiaoyan"    口癖 "哈喽哈喽～元气满满！"
#         "senpai"     学长     声线 "x4_jingjing"   口癖 "要好好学习哦"
#     三个参数按 __init__ 的顺序写：先名字，再声线，最后口癖。每一项后面写逗号。
#
# 用得上的写法：
#     "tsundere": Character("傲娇酱", "x4_yezi", "哼，才不是特意来陪你呢！"),
#         冒号左边是键，右边造出一位伙伴。造一次，就调用一次 __init__。
#
# 写对时：
#     左边出现三张卡片，顶上显示「已登记 3 位伙伴」。运行窗口打出三行「登记核对」。
# --- 以上 ---
ROLES = {
"tsundere": Character("傲娇酱", "x4_yezi", "哼，才不是特意来陪你呢！"),
"genki": Character("元气酱", "x4_xiaoyan", "哈喽哈喽～元气满满！"),
"senpai":Character("学长", "x4_jingjing", "要好好学习哦"),
}


def get_role(key):
    """按键取出一位伙伴。键不对时用元气酱；ROLES 还是空的就得到 None。"""
    return ROLES.get(key) or ROLES.get("genki")


def respond(role_key, msg):
    """让 role_key 这一位回一句话。页面点「发送」时调用它，它再去调用这一位伙伴自己的 respond 方法。"""
    role = get_role(role_key)
    if role is None:
        raise ValueError("ROLES 还是空的，先在 services.py 里登记三位伙伴")
    return role.respond(msg)


def speak(text, voice, save_path):
    """用 voice 这种声线把 text 念出来，声音存到 save_path。成功时得到 True。"""
    return tts_say(text, save_path=save_path, voice=voice)
