# -*- coding:utf-8 -*-
"""快递柜。"""


class Locker:
    """驿站的一格快递柜。快递、取件码、输错次数都藏在柜子里面。"""

    next_code = 2048

    def __init__(self, no):
        self.no = no
        self.__parcel = ""
        self.__code = 0
        self.__wrong = 0

    def put(self, parcel):
        """放进一件快递，return 发给收件人的取件码。"""
        self.__parcel = parcel
        self.__code = Locker.next_code
        Locker.next_code = Locker.next_code + 1
        return self.__code

    def pick(self, code):
        """输入取件码取件。输错 3 次就锁柜。return 这一次的结果。"""
        if self.__wrong >= 3:
            return self.no + " 已锁定，请找驿站工作人员"
        if code != self.__code:
            self.__wrong = self.__wrong + 1
            if self.__wrong == 3:
                return "取件码不对，" + self.no + " 已锁定"
            return "取件码不对，还能试 " + str(3 - self.__wrong) + " 次"
        parcel = self.__parcel
        self.__parcel = ""
        self.__code = 0
        self.__wrong = 0
        return self.no + " 开门，请取走 " + parcel

    @property
    def wrong(self):
        """输错了几次。外面只能看，不能改。"""
        return self.__wrong

    @property
    def empty(self):
        """柜子是不是空的。"""
        return self.__parcel == ""


a03 = Locker("A03")
a07 = Locker("A07")
code1 = a03.put("蓝牙耳机")
code2 = a07.put("机械键盘")
print("短信：A03 取件码 " + str(code1))
print("短信：A07 取件码 " + str(code2))

print(a03.pick(1234))
print(a03.pick(2048))
print("A03 空着吗：" + str(a03.empty))

print(a07.pick(1111))
print(a07.pick(2222))
print(a07.pick(3333))
print(a07.pick(2049))
print("A07 输错次数：" + str(a07.wrong))

try:
    print(a07.__code)
except AttributeError:
    print("取件码藏在柜子里，外面看不到")
try:
    a07.wrong = 0
except AttributeError:
    print("输错次数只能看，不能改")
