# -*- coding:utf-8 -*-
"""
iflytek_kit — 讯飞能力封装（本课用到语音合成与星火对话）。
tts_say：文字 → 语音文件；spark_chat：提示词 → 回复文本。
钥匙写在 app.py 所在文件夹的 .env 里；没填也能运行，用演示结果代替。
"""
from . import auth, client, config, mock
from .api_func import spark_chat, tts_say

__all__ = ["tts_say", "spark_chat", "auth", "client", "config", "mock"]
