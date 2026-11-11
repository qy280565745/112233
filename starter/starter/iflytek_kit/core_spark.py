# -*- coding:utf-8 -*-
"""
core_spark.py — 星火大模型内核：提问一次，交回回复文本。
一般经 iflytek_kit.spark_chat 调用；真实调用需 requests。
"""
import json

from . import client

_APPID, _API_KEY, _API_SECRET = client.creds("spark")

_URL = "https://spark-api-open.xf-yun.com/x2/chat/completions"

def spark_chat(question, appid=None, api_key=None, api_secret=None,
               model="spark-x", max_tokens=1024, temperature=0.5, url=None):
    """向星火提问一次；成功交回回复文本，失败交回 None。"""
    _api_key = api_key or _API_KEY
    _api_secret = api_secret or _API_SECRET
    _url = url or _URL

    if not question or not question.strip():
        print("[星火错误] 问题不能为空")
        return None
    if not (_api_key and _api_secret):
        print("[星火错误] 讯飞凭证未填写")
        return None

    headers = {
        "Authorization": f"Bearer {_api_key}:{_api_secret}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }

    try:
        requests = client.lazy_import("requests")
        resp = requests.post(_url, headers=headers, json=body, timeout=60)
        result = json.loads(resp.content.decode("utf-8"))
        if resp.status_code != 200 or result.get("code", 0) != 0:
            message = result.get("message") or result.get("error", {}).get("message") or result
            print(f"[星火错误] {message}")
            return None
        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return None
    except Exception as e:
        print(f"[星火错误] {e}")
        return None

if __name__ == "__main__":
    reply = spark_chat("用一句话介绍你自己")
    print(f"星火回复：{reply}")
