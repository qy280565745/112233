# -*- coding:utf-8 -*-
"""
ai_lab.py：星火回话和自建伙伴。这个文件已经写好，不要改。
ai_reply 把伙伴的名字、口癖、好感写进提示词，让星火替这一位回话。
create_role 用 Character 的 check_name 检查名字、用 from_dict 造出新伙伴，再存进 data/custom_roles.json。这两个方法是第2课的挑战题。
先问星火 X2。X2 没有正文，再问基础版。基础版也没有，回话换成这一位的口癖，页面照样能聊。
勾上 ✨AI 时，回话由星火给出，不经过 characters.py 里的 respond。
"""
import json
import os
import re

from iflytek_kit import mock, spark_chat

VOICES = ["x4_yezi", "x4_xiaoyan", "x4_jingjing"]
_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "data")
_SAVED = os.path.join(_DATA, "custom_roles.json")
NEED = "自建伙伴要用 Character 的 check_name 和 from_dict，这两个方法是第2课的挑战题，写好才能造新伙伴。"


def _love_of(role):
    try:
        love = getattr(role, "love", 0)
    except Exception as e:
        print("这里出错了（读好感）：", type(e).__name__, e)
        return 0
    return love if isinstance(love, int) else 0


def _mood(love):
    if love >= 80:
        return "你们已经非常亲密，语气撒娇、主动、带点小甜蜜"
    if love >= 40:
        return "你们已经熟悉，语气热络自然，像关系很好的朋友"
    return "你们刚认识不久，保持人设，语气略带距离感"


def ai_reply(role, msg):
    """让星火按这一位的人设回一句。写了 add_love 时，每聊一句好感加 1。"""
    if role is None:
        return "还没有伙伴，先在 services.py 里登记。"
    name = getattr(role, "name", None) or "语音伙伴"
    catchphrase = getattr(role, "catchphrase", None) or ""
    persona = getattr(role, "persona", "") or ""
    add = getattr(role, "add_love", None)
    if callable(add):
        try:
            add(1)
        except Exception as e:
            print("这里出错了（add_love）：", type(e).__name__, e)
    love = _love_of(role)
    prompt = (
        "你在扮演一个二次元语音伙伴。角色名：%s；口癖：「%s」；%s"
        "当前好感度 %d/100（%s）。请完全代入角色，用角色的语气回应用户这句话，"
        "自然带上口癖，40字以内，只输出回应本身：%s"
        % (name, catchphrase, ("人设：" + persona + "；") if persona else "",
           love, _mood(love), msg)
    )
    text = spark_chat(prompt)
    if not text or not str(text).strip():
        print("星火 X2 没有回，改用基础版。")
        text = spark_chat(
            prompt,
            model="lite",
            url="https://spark-api-open.xf-yun.com/v1/chat/completions",
        )
    if not text or not str(text).strip() or str(text).strip() == mock.MOCK_SPARK_TEXT:
        return "（星火没有连上，先用口癖回你）" + catchphrase
    # 星火有时会在括号里加动作或旁白，去掉以后再显示、再念
    text = re.sub(r"[（(][^（）()]*[）)]", "", str(text)).strip()
    return text or catchphrase


def _new_key(roles):
    n = 1
    while ("custom_%d" % n) in roles:
        n += 1
    return "custom_%d" % n


def _tools(svc):
    """拿到 Character 上的 check_name 和 from_dict。少一个就造不了。"""
    cls = getattr(svc, "Character", None)
    check = getattr(cls, "check_name", None)
    build = getattr(cls, "from_dict", None)
    if callable(check) and callable(build):
        return check, build
    return None, None


def create_role(svc, name, voice, catchphrase, persona):
    """页面上点「造出来！」时调用。成功时左边多一位伙伴。"""
    check, build = _tools(svc)
    if check is None:
        return {"ok": False, "msg": NEED}
    try:
        ok, why = check(name)
    except Exception as e:
        print("这里出错了（check_name）：", type(e).__name__, e)
        return {"ok": False, "msg": "check_name 要 return 两个值，例如 return False, \"名字不能是空的\""}
    if not ok:
        return {"ok": False, "msg": why or "名字不合格"}
    catchphrase = (catchphrase or "").strip()[:30]
    if not catchphrase:
        return {"ok": False, "msg": "口癖不能是空的，伙伴说话要带上它"}
    data = {"name": name.strip(), "voice": voice if voice in VOICES else VOICES[0],
            "catchphrase": catchphrase}
    try:
        role = build(data)
    except Exception as e:
        print("这里出错了（from_dict）：", type(e).__name__, e)
        return {"ok": False, "msg": "from_dict 出错了，看运行窗口里最后几行"}
    if role is None:
        return {"ok": False, "msg": "from_dict 要 return cls(...) 造出来的伙伴"}
    role.persona = (persona or "").strip()[:50]
    key = _new_key(svc.ROLES)
    svc.ROLES[key] = role
    saved = _load_saved()
    saved.append(dict(data, key=key, persona=role.persona))
    os.makedirs(_DATA, exist_ok=True)
    with open(_SAVED, "w", encoding="utf-8") as f:
        json.dump(saved, f, ensure_ascii=False, indent=2)
    print("自建伙伴核对：" + str(role))
    return {"ok": True, "key": key}


def _load_saved():
    try:
        with open(_SAVED, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def load_custom_roles(svc):
    """启动时把 data/custom_roles.json 里存着的自建伙伴，用 from_dict 再造出来。"""
    saved = _load_saved()
    if not saved:
        return
    check, build = _tools(svc)
    if build is None:
        print("data/custom_roles.json 里有自建伙伴。写好 from_dict 以后，重新运行才会出现。")
        return
    for item in saved:
        key = item.get("key") or _new_key(svc.ROLES)
        if key in svc.ROLES:
            continue
        try:
            role = build(item)
        except Exception as e:
            print("这里出错了（from_dict）：", type(e).__name__, e)
            continue
        role.persona = item.get("persona", "")
        svc.ROLES[key] = role
