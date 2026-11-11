# -*- coding:utf-8 -*-
"""
config.py — 从 .env 读取讯飞凭证。
从本文件所在目录逐级向上找 .env，近处覆盖远处；都没有则交回空。
"""
import os
from pathlib import Path

_SERVICES = {
    "tts":   ("IFLYTEK_TTS_APPID",   "IFLYTEK_TTS_API_KEY",   "IFLYTEK_TTS_API_SECRET"),
    "stt":   ("IFLYTEK_ASR_APPID",   "IFLYTEK_ASR_API_KEY",   "IFLYTEK_ASR_API_SECRET"),
    "ocr":   ("IFLYTEK_OCR_APPID",   "IFLYTEK_OCR_API_KEY",   "IFLYTEK_OCR_API_SECRET"),
    "trans": ("IFLYTEK_TRANS_APPID", "IFLYTEK_TRANS_API_KEY", "IFLYTEK_TRANS_API_SECRET"),
    "face":  ("IFLYTEK_FACE_APPID",  "IFLYTEK_FACE_API_KEY",  "IFLYTEK_FACE_API_SECRET"),
    "spark": ("IFLYTEK_SPARK_APPID", "IFLYTEK_SPARK_API_KEY", "IFLYTEK_SPARK_API_SECRET"),
}

_loaded = False

def _iter_env_files():
    """从 kit 目录往上收集所有 .env 路径，近处在前。"""
    d = Path(__file__).resolve().parent
    seen = set()
    while True:
        cand = d / ".env"
        key = str(cand.resolve()) if cand.exists() else str(cand)
        if cand.is_file() and key not in seen:
            seen.add(key)
            yield cand
        if d.parent == d:
            break
        d = d.parent

def _parse_pairs(path):
    """手工解析 .env 里的 KEY=VALUE 行。"""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            yield key, value

def load():
    """把找到的 .env 载入环境变量（只执行一次）。"""
    global _loaded
    if _loaded:
        return
    _loaded = True
    preset = {k for k, v in os.environ.items() if v}
    files = list(_iter_env_files())
    for path in reversed(files):
        for key, value in _parse_pairs(path):
            if not value:
                continue
            if key in preset:
                continue
            os.environ[key] = value

def get_creds(service):
    """交回某个服务的三项钥匙；没填的项是 None。"""
    load()
    keys = _SERVICES.get(service)
    if not keys:
        return None, None, None
    return tuple(os.environ.get(k) for k in keys)

def has_creds(service):
    """这个服务的三项钥匙是不是都填好了。"""
    appid, key, secret = get_creds(service)
    return bool(appid and key and secret)
