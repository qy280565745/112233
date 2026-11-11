# -*- coding:utf-8 -*-
"""
次元语音伙伴 · 第1课：写出伙伴类 Character。
页面上的每一位伙伴，都是用 Character 这个类造出来的一个对象。
这一课先在这个文件里写好 Character，再到 services.py 里用它造出傲娇酱、元气酱、学长三位。
class Character: 这一行已经写好。类属性和每个方法都写在它下面，缩进 4 格，def 那一行也自己写。
每一段代码写在这一段「# --- 以上 ---」的下面、下一段「# --- 请完成 ---」的上面。
方法名和参数照每一段写，网页才找得到它们。
写完保存，在 PyCharm 里运行 app.py，浏览器打开 http://127.0.0.1:5000 。
每一段写着：页面上哪里会变、要做的事、写对时的结果。要用到新写法时，「用得上的写法」里给出那一行怎么写。
这个文件只写类。不要在下面造伙伴或 print：app.py 每次启动都会读这个文件，多造一位，顶上的登记数就多加 1。
想试一试写得对不对，右键运行 自查.py。
"""


class Character:
    """一位语音伙伴。名字、声线、口癖、好感、聊过的话，都记在这一位自己身上。"""

    # --- 请完成 ---
    # TODO[第1课-基础] 类属性 count，和构造方法 __init__(self, name, voice, catchphrase)
    #
    # 页面上：网页顶上的「已登记 3 位伙伴」读的是 Character.count。
    #         左边每张卡片上的名字、♥ 后面的数字，读的是这一位自己的 name 和 love。
    #
    # 要做的事：
    #     1. 在这一段「# --- 以上 ---」的下面、所有方法的外面，写类属性 count = 0。三位伙伴共用这一个数。
    #     2. 写 __init__，第一个参数是 self，后面依次是 name、voice、catchphrase。
    #     3. 把三个参数存到 self 上：self.name、self.voice、self.catchphrase。
    #        voice 是这一位的声线，讯飞按它选发音人；catchphrase 是这一位的口癖，说话时接在句尾。
    #     4. 写 self.love = 0。好感从 0 开始，每一位各算各的。
    #     5. 写 self.history = []。聊过的话按顺序存进这个列表：respond 把每句话存进来，recall 从这里数句数。
    #     6. 最后写 Character.count = Character.count + 1。每造出一位伙伴，登记数加 1。
    #
    # 用得上的写法：
    #     Character.count = Character.count + 1
    #         改的是类上那一个 count。写成 self.count = self.count + 1，
    #         只是给这一位自己加了一个 count，类上的 count 还是 0，顶上就一直显示「已登记 0 位伙伴」。
    #
    # 写对时：
    #     Character("傲娇酱", "x4_yezi", "哼") 造出来以后，它的 name 是「傲娇酱」，love 是 0，history 是 []。
    #     造两位以后，Character.count 是 2。
    # --- 以上 ---
    count = 0
    def __init__(self, name, voice, catchphrase):
        self.name = name
        self.voice = voice
        self.catchphrase = catchphrase
        self.love = 0
        self.history = []
        Character.count = Character.count + 1





    # --- 请完成 ---
    # TODO[第1课-基础] greet(self)
    #
    # 页面上：点左边的一位伙伴，聊天框里先出来这一位的招呼，讯飞用这一位的声线念出来。
    #
    # 要做的事：
    #     return "我是" + self.name + "，" + self.catchphrase。
    #     不要 print，页面拿的是 return 出来的那一句。
    #
    # 写对时：
    #     名字「傲娇酱」、口癖「哼，才不是特意来陪你呢！」的伙伴，greet() 得到
    #     「我是傲娇酱，哼，才不是特意来陪你呢！」。
    # --- 以上 ---
    def greet(self):
        return "我是" + self.name + "，" + self.catchphrase

    # --- 请完成 ---
    # TODO[第1课-进阶] respond(self, msg)
    #
    # 页面上：在输入框里打字、点「发送」，聊天框里出来的那一句回话。
    #         说的话里有「夸夸」时，♥ 后面的数字加 10，还会飘出一颗心。
    #
    # msg 是你在输入框里打的那句话，例如「快夸夸我」。
    #
    # 要做的事：
    #     1. 先把这句话存起来：self.history.append(msg)。
    #     2. msg 里有「夸夸」：好感加 10，加完大于 100 就改回 100。return "被夸啦，好开心！" + self.catchphrase
    #     3. msg 里有「难过」：return "别难过，有我陪着你呢。" + self.catchphrase
    #     4. msg 里有「再见」：return "拜拜～记得想我。" + self.catchphrase
    #     5. 都没有：return "嗯嗯，" + self.catchphrase
    #
    # 用得上的写法：
    #     "夸夸" in msg                    msg 里有「夸夸」这两个字时成立。
    #     self.love = self.love + 10       改的是这一位自己的好感，另外两位不变。
    #
    # 写对时：
    #     对傲娇酱说「快夸夸我」，回话是「被夸啦，好开心！哼，才不是特意来陪你呢！」，♥ 从 0 变成 10。
    #     连说 12 次「夸夸」，♥ 停在 100。换到元气酱，她的 ♥ 还是 0。
    #     试的时候不要勾 ✨AI：勾上以后回话由星火给出，不经过这里的 respond。
    #     回话里的标点要和上面一模一样，用中文的逗号、感叹号；直接复制这里的句子最稳。
    # --- 以上 ---
    def respond(self, msg):
        self.history.append(msg)
        if  "夸夸" in msg:
            self.love = self.love + 10
            if self.love > 100:
                self.love = 100
            return "被夸啦，好开心！" + self.catchphrase
        elif "难过" in msg:
            return "别难过，有我陪着你呢。" + self.catchphrase
        elif "再见" in msg:
            return "拜拜～记得想我。" + self.catchphrase
        else:
            return "嗯嗯，" + self.catchphrase


    # --- 请完成 ---
    # TODO[第1课-进阶] __str__(self)
    #
    # 页面上：伙伴名字下面那一行「名牌」。名牌显示的就是 str(这一位)。
    #         没写 __str__ 时，名牌是一串 <characters.Character object at 0x...>，那是这个对象在内存里的地址。
    #         运行窗口里启动时打出的「登记核对」也是这一句。
    #
    # 要做的事：
    #     return self.name + " / " + self.catchphrase。
    #
    # 写对时：
    #     傲娇酱的名牌是「傲娇酱 / 哼，才不是特意来陪你呢！」。print(这一位) 打出的也是这一句。
    # --- 以上 ---
    def  __str__(self):
        return self.name + " / " + self.catchphrase
    # --- 请完e成 ---
    # TODO[第1课-挑战] recall(self)
    #
    # 页面上：点输入框右边的 📜，伙伴说出你们聊了几句、你最后说的是什么。
    #
    # 要做的事：
    #     1. self.history 里一句都没有：return "我们还没聊过天呢。"
    #     2. 否则 return "我们聊了 2 句。你最后说的是：夸夸我" 这样一句。
    #        2 是 history 里有几句，「夸夸我」是 history 里的最后一句。
    #
    # 用得上的写法：
    #     len(self.history)      列表里有几项。
    #     self.history[-1]       列表的最后一项。
    #
    # 写对时：
    #     先对伙伴说「你好」「夸夸我」，再点 📜，伙伴说「我们聊了 2 句。你最后说的是：夸夸我」。
    #     试的时候不要勾 ✨AI，勾上以后聊的话不会存进 history。
    # --- 以上 ---
    def recall(self):
        if len(self.history) <= 0:
            return "我们还没聊过天呢。"

        return "我们聊了" + str(len(self.history)) + "你最后说的是：" + self.history[-1] +" 这样一句。"