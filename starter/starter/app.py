# -*- coding:utf-8 -*-
"""
次元语音伙伴。运行后打开 http://127.0.0.1:5000 。
点左边的一位伙伴，它先打招呼；在下面打字聊天，它按 characters.py 里写的方法回话。
伙伴的类写在 characters.py，三位伙伴登记在 services.py。这个文件不要改，也不要把钥匙写进来。
"""
import os
import sys
import wave

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from flask import Flask, jsonify, render_template, request

import services
import ai_lab

app = Flask(__name__)
_HERE = os.path.dirname(os.path.abspath(__file__))
_STATIC = os.path.join(_HERE, "static")
_FACES = {"tsundere": "😤", "genki": "😊", "senpai": "📚"}
_played = [0]


def _text(value):
    """只收字符串。方法没写、或者 return 的不是字符串，都当作没有。"""
    return value if isinstance(value, str) else None


def _love(role):
    """读这一位的好感。读不到时按 0。"""
    try:
        love = getattr(role, "love", 0)
    except Exception as e:
        print("这里出错了（读好感）：", type(e).__name__, e)
        return 0
    return love if isinstance(love, int) else 0


def _count():
    """读类属性 Character.count。还没写时得到 None。"""
    cls = getattr(services, "Character", None)
    n = getattr(cls, "count", None)
    return n if isinstance(n, int) else None


def _tag(role):
    """名牌就是 str(这一位)。写了 __str__ 才是一句话。"""
    try:
        return str(role)
    except Exception as e:
        print("这里出错了（__str__）：", type(e).__name__, e)
        return None


def _call(role, name, *args):
    """调用这一位的某个方法，拿到它 return 的那句话。"""
    fn = getattr(role, name, None)
    if not callable(fn):
        return None
    try:
        return _text(fn(*args))
    except Exception as e:
        print("这里出错了（" + name + "）：", type(e).__name__, e)
        return None


def _roles():
    roles = getattr(services, "ROLES", None)
    return roles if isinstance(roles, dict) else {}


def _audio(role, text):
    """用这一位的声线把 text 念出来，存成网页能播的 wav。"""
    if not text or role is None:
        return None
    os.makedirs(_STATIC, exist_ok=True)
    voice = getattr(role, "voice", None) or "x4_yezi"
    pcm = os.path.join(_STATIC, "role.pcm")
    wav = os.path.join(_STATIC, "role.wav")
    try:
        ok = services.speak(text, voice, pcm)
    except Exception as e:
        print("这里出错了（speak）：", type(e).__name__, e)
        return None
    if not ok or not os.path.exists(pcm):
        return None
    with open(pcm, "rb") as f:
        frames = f.read()
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(frames)
    _played[0] += 1
    return "/static/role.wav?n=" + str(_played[0])


def _report():
    """启动时在运行窗口打出登记核对。"""
    n = _count()
    print("已登记 " + (str(n) if n is not None else "?") + " 位伙伴")
    for role in _roles().values():
        print("登记核对：" + str(_tag(role)))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/roles")
def api_roles():
    """左边的卡片、顶上的登记数、名牌，都从这里读。"""
    roles = []
    for key, role in _roles().items():
        roles.append({
            "key": key,
            "name": _text(getattr(role, "name", None)) or "?",
            "love": _love(role),
            "tag": _tag(role),
            "face": _FACES.get(key, "🎀"),
        })
    return jsonify({"count": _count(), "roles": roles})


@app.route("/api/greet")
def api_greet():
    """点一位伙伴时，它先打招呼。"""
    role = services.get_role(request.args.get("role", "genki"))
    text = _call(role, "greet") if role is not None else None
    return jsonify({"text": text, "audio": _audio(role, text)})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """点「发送」：按 respond 里写的回法回一句。"""
    data = request.get_json() or {}
    key = str(data.get("role", "genki"))
    msg = str(data.get("msg", ""))
    role = services.get_role(key)
    try:
        text = _text(services.respond(key, msg))
    except Exception as e:
        print("这里出错了（respond）：", type(e).__name__, e)
        text = None
    if text is None:
        text = "【提示】这一位没回出话：respond 还没写，或者运行出错了。看运行窗口里「这里出错了」那一行，再重新运行 app.py。"
    print(str(getattr(role, "name", "?")) + " 收到「" + msg + "」，好感 " + str(_love(role)))
    return jsonify({"text": text, "audio": _audio(role, text), "love": _love(role)})


@app.route("/api/recall")
def api_recall():
    """点 📜：伙伴说出你们聊了几句。"""
    role = services.get_role(request.args.get("role", "genki"))
    text = _call(role, "recall") if role is not None else None
    return jsonify({"text": text, "audio": _audio(role, text)})


@app.route("/api/hack", methods=["POST"])
def api_hack():
    """点「直接改成 999」：试着在外面写 role.love = 999。"""
    data = request.get_json() or {}
    role = services.get_role(str(data.get("role", "genki")))
    if role is None:
        return jsonify({"ok": False, "msg": "还没有伙伴", "love": 0})
    try:
        role.love = 999
    except AttributeError:
        return jsonify({"ok": False, "msg": "好感已上锁，只能靠聊天慢慢涨", "love": _love(role)})
    return jsonify({"ok": True, "msg": "好感被直接改成了 999，这个数已经不可信了", "love": _love(role)})


@app.route("/api/chat_ai", methods=["POST"])
def api_chat_ai():
    """勾上 ✨AI：星火读这一位的名字、口癖和好感来回话。"""
    data = request.get_json() or {}
    key = str(data.get("role", "genki"))
    role = services.get_role(key)
    text = ai_lab.ai_reply(role, str(data.get("msg", "")))
    return jsonify({"text": text, "audio": _audio(role, text), "love": _love(role), "ai": True})


@app.route("/api/roles/create", methods=["POST"])
def api_role_create():
    """「＋ 自建伙伴」：用 check_name 检查名字，用 from_dict 造出新伙伴。"""
    data = request.get_json() or {}
    result = ai_lab.create_role(
        services,
        str(data.get("name", "")),
        str(data.get("voice", "")),
        str(data.get("catchphrase", "")),
        str(data.get("persona", "")),
    )
    return jsonify(result)


if __name__ == "__main__":
    ai_lab.load_custom_roles(services)
    _report()
    app.run(host="127.0.0.1", port=5000, debug=False)
