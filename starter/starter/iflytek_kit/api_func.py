# -*- coding:utf-8 -*-
"""
api_func.py — 对外调用入口：tts_say 合成语音，spark_chat 问星火。
没钥匙或调用失败时自动走本地演示结果。
"""
from . import client, core_spark, core_tts, mock

def tts_say(text, save_path=None, voice="x4_yezi", speed=50, volume=50, pitch=50, **kw):
    """文字合成语音并保存；成功交回 True。没填钥匙或连不上时，用一小段演示声音代替。"""
    if client.mock_mode("tts"):
        return mock.say_fallback(text, save_path or "_mock.pcm")
    try:
        ok = core_tts.speak(text, save_path=save_path, vcn=voice,
                            speed=speed, volume=volume, pitch=pitch, play=False, **kw)
    except Exception as e:
        print("这里出错了（tts_say）：", type(e).__name__, e)
        return mock.say_fallback(text, save_path or "_mock.pcm")
    if ok:
        return ok
    print("这里出错了（tts_say）：合成没有成功")
    return mock.say_fallback(text, save_path or "_mock.pcm")

def spark_chat(prompt, **kw):
    """把提示词交给星火，交回回复文本；没钥匙或失败时交回预置文案。"""
    if client.mock_mode("spark"):
        return mock.MOCK_SPARK_TEXT
    try:
        return core_spark.spark_chat(prompt, **kw)
    except Exception as e:
        print("这里出错了（spark_chat）：", type(e).__name__, e)
        return mock.MOCK_SPARK_TEXT
