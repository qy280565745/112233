# -*- coding:utf-8 -*-
"""
mock.py — 演示结果：没填钥匙、连不上，或者设了 IFLYTEK_MOCK=1 时，交回事先准备好的结果。
对外调用仍走同一套函数名，页面上能继续演示。
"""
import math
import os
import struct

# ---------- 触发开关 ----------

def forced():
    """环境变量 IFLYTEK_MOCK=1 时，一律用演示结果。"""
    return os.environ.get("IFLYTEK_MOCK") == "1"

# ---------- 预置数据 ----------
MOCK_SPARK_TEXT = "星火没有连上，这是一句演示回复。"

# ---------- 演示声音（能播放的一小段「滴」声） ----------

def mock_pcm(save_path, seconds=0.6):
    """写出一段可播放的短 PCM 到指定路径，交回 True。"""
    rate = 16000
    n = int(rate * seconds)
    freq = 660.0
    frames = bytearray()
    for i in range(n):
        t = i / rate
        env = 1.0 - (i / n) ** 2            # 渐弱包络，避免爆音
        v = int(12000 * env * math.sin(2 * math.pi * freq * t))
        frames += struct.pack("<h", v)
    with open(save_path, "wb") as f:
        f.write(bytes(frames))
    return True

def say_fallback(text, save_path):
    """没法真的合成时，把一小段演示声音写到 save_path。"""
    return mock_pcm(save_path)
