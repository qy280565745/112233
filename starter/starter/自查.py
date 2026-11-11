# -*- coding:utf-8 -*-
"""
第1课自查：在 PyCharm 里右键运行这个文件。
它会照着 characters.py 和 services.py 里每一段「写对时」试一遍。
每一行前面是 ✅ 就是写对了；是 ❌ 时，后面写着去看哪一段。这个文件不会改你写的代码。
每一行前面标着基础、进阶或挑战。最后分开数：你做到哪一档，就看那一档是不是全对。
回话要和备注里的句子一字不差，标点也要一样，例如中文的逗号「，」和感叹号「！」。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

LEVELS = ["基础", "进阶", "挑战"]
bad = {level: 0 for level in LEVELS}
total = {level: 0 for level in LEVELS}


def check(level, name, ok, hint):
    print(("✅ " if ok else "❌ ") + "［" + level + "］" + name + ("" if ok else "　→ " + hint))
    total[level] += 1
    if not ok:
        bad[level] += 1


def attempt(fn):
    try:
        return fn()
    except Exception as e:
        return e


try:
    from characters import Character
except Exception as e:
    print("❌ characters.py 一运行就出错：" + type(e).__name__ + " " + str(e))
    print("先看运行窗口里报错写的是哪一行，改好再运行自查。")
    sys.exit(1)

start = getattr(Character, "count", None)
c = attempt(lambda: Character("测试酱", "x4_yezi", "喵"))
made = not isinstance(c, Exception)
check("基础", "Character(名字, 声线, 口癖) 能造出伙伴", made, "看 __init__ 那一段：def __init__(self, name, voice, catchphrase)")
check("基础", "名字、声线、口癖存在 self 上",
      made and getattr(c, "name", None) == "测试酱" and getattr(c, "voice", None) == "x4_yezi"
      and getattr(c, "catchphrase", None) == "喵", "看 __init__ 第 3 步")
check("基础", "好感从 0 开始", made and getattr(c, "love", None) == 0, "看 __init__ 第 4 步：self.love = 0")
check("基础", "history 是空列表", made and getattr(c, "history", None) == [], "看 __init__ 第 5 步：self.history = []")
attempt(lambda: Character("再造一位", "x4_yezi", "喵"))
check("基础", "类属性 count 每造一位加 1",
      isinstance(start, int) and getattr(Character, "count", None) == start + 2,
      "看 __init__ 第 1 步和第 6 步：写 Character.count = Character.count + 1，不要写 self.count")

if made:
    check("基础", "greet 是「我是测试酱，喵」", attempt(c.greet) == "我是测试酱，喵" if hasattr(c, "greet") else False,
          "看 greet 那一段：要 return，不要 print；逗号是中文的「，」")
    r = attempt(lambda: c.respond("快夸夸我")) if hasattr(c, "respond") else None
    check("进阶", "夸夸：回「被夸啦，好开心！」后面接上口癖", r == "被夸啦，好开心！喵", "看 respond 第 2 步，标点照抄备注里的句子")
    check("进阶", "夸夸：好感加 10", getattr(c, "love", None) == 10, "看 respond 第 2 步：self.love = self.love + 10")
    check("进阶", "难过、再见、别的话各回一句",
          hasattr(c, "respond") and attempt(lambda: c.respond("我好难过")) == "别难过，有我陪着你呢。喵"
          and attempt(lambda: c.respond("再见啦")) == "拜拜～记得想我。喵"
          and attempt(lambda: c.respond("今天下雨")) == "嗯嗯，喵", "看 respond 第 3、4、5 步，标点照抄备注里的句子")
    for _ in range(12):
        attempt(lambda: c.respond("夸夸"))
    check("进阶", "好感最多 100", getattr(c, "love", None) == 100, "看 respond 第 2 步：大于 100 改回 100")
    check("进阶", "说过的话存进 history", isinstance(getattr(c, "history", None), list) and len(c.history) == 16,
          "看 respond 第 1 步：self.history.append(msg)")
    check("进阶", "__str__ 是「测试酱 / 喵」", attempt(lambda: str(c)) == "测试酱 / 喵",
          "看 __str__ 那一段：要 return 一句话，不要 print")
    d = attempt(lambda: Character("回忆酱", "x4_yezi", "的说"))
    if not isinstance(d, Exception) and hasattr(d, "recall") and hasattr(d, "respond"):
        first = attempt(d.recall)
        attempt(lambda: d.respond("你好"))
        attempt(lambda: d.respond("夸夸我"))
        check("挑战", "recall：还没聊时", first == "我们还没聊过天呢。", "看 recall 第 1 步")
        check("挑战", "recall：聊了 2 句", attempt(d.recall) == "我们聊了 2 句。你最后说的是：夸夸我", "看 recall 第 2 步")
    else:
        check("挑战", "recall", False, "看 recall 那一段")

services = attempt(lambda: __import__("services"))
if isinstance(services, Exception):
    print("❌ services.py 一运行就出错：" + type(services).__name__ + " " + str(services))
    roles = {}
else:
    roles = getattr(services, "ROLES", {})
check("基础", "ROLES 里有 tsundere、genki、senpai 三项",
      isinstance(roles, dict) and sorted(roles) == ["genki", "senpai", "tsundere"], "看 services.py 的 ROLES")
want = {"tsundere": ("傲娇酱", "x4_yezi"), "genki": ("元气酱", "x4_xiaoyan"), "senpai": ("学长", "x4_jingjing")}
check("基础", "三位的名字和声线照表写",
      isinstance(roles, dict) and all(getattr(roles.get(k), "name", None) == v[0]
                                      and getattr(roles.get(k), "voice", None) == v[1] for k, v in want.items()),
      "看 services.py 的 ROLES：先名字，再声线，最后口癖")

print()
for level in LEVELS:
    if total[level] == 0:
        print(level + "：要先写好 __init__，才能检查这一档。")
    elif bad[level] == 0:
        print(level + "：" + str(total[level]) + " 项全对。")
    else:
        print(level + "：还有 " + str(bad[level]) + " 项没写对。")
if bad["基础"] == 0:
    print("基础写对了，运行 app.py，到网页上点一点。")
