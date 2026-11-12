# -*- coding:utf-8 -*-
"""网盘会员。"""


class CloudDisk:
    """普通用户的网盘。容量 100 GB，下载每秒 100 KB。"""

    def __init__(self, user, used):
        self.user = user
        self.used = used
        self.space = 100
        self.speed = 100

    def minutes(self, size):
        """下载 size MB 的文件要几分钟，保留一位小数。"""
        return round(size * 1024 / self.speed / 60, 1)

    def save(self, size):
        """再存 size GB。超出容量就存不进去。return 这一次的结果。"""
        if self.used + size > self.space:
            return (self.user + " 空间不够，还差 "
                    + str(self.used + size - self.space) + " GB")
        self.used = self.used + size
        return self.user + " 存好了，已用 " + str(self.used) + " GB"

    def card(self):
        """return 这个用户的会员卡片。"""
        return (self.user + " 普通用户 已用 "
                + str(self.used) + "/" + str(self.space) + " GB")


class VipDisk(CloudDisk):
    """超级会员。比普通用户多一个剩余月数，容量 5120 GB，下载每秒 20480 KB。"""

    def __init__(self, user, used, months):
        super().__init__(user, used)
        self.months = months
        self.space = 5120
        self.speed = 20480

    def card(self):
        return (self.user + " 超级会员 还剩 " + str(self.months) + " 个月"
                + " 已用 " + str(self.used) + "/" + str(self.space) + " GB")


class StudentVip(VipDisk):
    """学生会员。也是超级会员，容量 2048 GB，下载每秒 10240 KB。"""

    def __init__(self, user, used, months):
        super().__init__(user, used, months)
        self.space = 2048
        self.speed = 10240

    def card(self):
        return super().card() + "（学生认证）"


disks = [CloudDisk("小林", 96),
         VipDisk("阿杰", 1200, 3),
         StudentVip("小美", 30, 10)]
for d in disks:
    print(d.card())

print("—— 下载 4096 MB 的课程视频 ——")
for d in disks:
    print(d.user + " 要 " + str(d.minutes(4096)) + " 分钟")

print("—— 再存 8 GB 的照片 ——")
for d in disks:
    print(d.save(8))

print("—— 谁是会员 ——")
for d in disks:
    if isinstance(d, VipDisk):
        print(d.user + " 是会员")
    else:
        print(d.user + " 不是会员")
print("小美的类型就是 VipDisk 吗：" + str(type(disks[2]) is VipDisk))
