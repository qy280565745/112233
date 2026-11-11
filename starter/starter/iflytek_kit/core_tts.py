# -*- coding:utf-8 -*-
"""
core_tts.py — 语音合成内核：文字 → PCM 音频文件，可选播放。
一般经 iflytek_kit.tts_say 调用；真实调用需 websocket-client。
"""
import base64
import hashlib
import hmac
import json
import os
import ssl
import wave
import _thread as thread
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

from . import client

_APPID, _API_KEY, _API_SECRET = client.creds("tts")

_HOST = "tts-api.xfyun.cn"
_PATH = "/v2/tts"

def _build_url(appid, api_key, api_secret):
    """生成带鉴权的 WebSocket 地址，供语音合成连接。"""
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = (
        "host: " + _HOST + "\n"
        "date: " + date + "\n"
        "GET " + _PATH + " HTTP/1.1"
    )
    signature_sha = hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    signature_sha = base64.b64encode(signature_sha).decode("utf-8")
    authorization_origin = (
        'api_key="%s", algorithm="%s", headers="%s", signature="%s"'
        % (api_key, "hmac-sha256", "host date request-line", signature_sha)
    )
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")
    params = {"authorization": authorization, "date": date, "host": _HOST}
    return "wss://" + _HOST + _PATH + "?" + urlencode(params)

# ================================================================
# 播放工具（零第三方依赖）
# ================================================================

def _pcm_to_wav(pcm_path, wav_path, sample_rate=16000):
    """给 PCM 补上 WAV 文件头，方便系统播放。"""
    with open(pcm_path, "rb") as f:
        pcm_data = f.read()
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm_data)

def play_pcm(pcm_path):
    """把 PCM 转成 WAV 并用系统播放器播放。"""
    try:
        import winsound
    except ImportError:
        print("[播放提示] 当前系统不支持 winsound，可手动打开转换出的 WAV 文件")
        return False
    wav_path = os.path.splitext(pcm_path)[0] + ".play.wav"
    try:
        _pcm_to_wav(pcm_path, wav_path)
        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        return True
    except Exception as e:
        print(f"[播放提示] 播放失败（可手动打开 WAV）：{e}")
        return False
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

# ================================================================
# 主接口
# ================================================================

def speak(text, appid=None, api_key=None, api_secret=None, save_path="./output.pcm",
          vcn="x4_yezi", speed=50, volume=50, pitch=50, play=True):
    """调用讯飞把文字合成 PCM 语音；成功交回 True，失败交回 None。"""
    _appid = appid or _APPID
    _api_key = api_key or _API_KEY
    _api_secret = api_secret or _API_SECRET

    if not text or not text.strip():
        print("[TTS错误] 要合成的文字不能为空")
        return None
    if not (_appid and _api_key and _api_secret):
        print("[TTS错误] 讯飞凭证未填写")
        return None

    ws_url = _build_url(_appid, _api_key, _api_secret)
    state = {"ok": False}

    def on_open(ws):
        """连接成功后发合成请求。"""
        def run(*args):
            """在子线程里把文字包发出去。"""
            body = {
                "common": {"app_id": _appid},
                "business": {
                    "aue": "raw",
                    "auf": "audio/L16;rate=16000",
                    "vcn": vcn,
                    "tte": "utf8",
                    "speed": speed,
                    "volume": volume,
                    "pitch": pitch,
                },
                "data": {
                    "status": 2,
                    "text": str(base64.b64encode(text.encode("utf-8")), "utf-8"),
                },
            }
            ws.send(json.dumps(body))
        thread.start_new_thread(run, ())

    def on_message(ws, message):
        """收到音频块就写入文件，收齐后关闭连接。"""
        try:
            if isinstance(message, (bytes, bytearray)):
                return
            msg = json.loads(message)
            code = msg.get("code", -1)
            data = msg.get("data", {})
            if code != 0:
                print(f"[TTS错误] 服务返回 code={code}")
                ws.close()
            else:
                audio = data.get("audio", "")
                if audio:
                    with open(save_path, "ab") as f:
                        f.write(base64.b64decode(audio))
                if data.get("status") == 2:
                    state["ok"] = True
                    ws.close()
        except Exception as e:
            print(f"[TTS错误] 处理响应失败: {e}")
            ws.close()

    def on_error(ws, error):
        """连接出错时打印原因。"""
        print(f"[TTS错误] {error}")

    if os.path.exists(save_path):
        os.remove(save_path)

    websocket = client.lazy_import("websocket", "websocket-client")
    ws = websocket.WebSocketApp(ws_url, on_open=on_open,
                                on_message=on_message, on_error=on_error)
    try:
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    except Exception as e:
        print(f"[TTS错误] {e}")
        return None

    ok = state["ok"]
    if ok and play:
        play_pcm(save_path)
    return True if ok else None

if __name__ == "__main__":
    ok = speak("你好，我是你的AI伙伴！", save_path="./demo_output.pcm")
    print("合成成功" if ok else "合成失败")
