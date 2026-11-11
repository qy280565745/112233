# -*- coding:utf-8 -*-
"""
auth.py — 讯飞开放平台 HMAC-SHA256 签名工具。
生成 WebSocket / HTTP 的鉴权 URL 或请求头，供语音与识别等接口使用。
"""
import base64
import hashlib
import hmac
import time
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

def _httpdate(dt):
    """把时间格式化成 RFC1123 字符串，供鉴权签名用。"""
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
        weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)

def build_ws_url(host, path, api_key, api_secret):
    """生成带鉴权的 WebSocket URL（语音合成等用）。"""
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = (
        "host: " + host + "\n"
        "date: " + date + "\n"
        "GET " + path + " HTTP/1.1"
    )
    signature_sha = base64.b64encode(hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()).decode("utf-8")
    authorization_origin = (
        'api_key="%s", algorithm="%s", headers="%s", signature="%s"'
        % (api_key, "hmac-sha256", "host date request-line", signature_sha)
    )
    authorization = base64.b64encode(
        authorization_origin.encode("utf-8")).decode("utf-8")
    params = {"authorization": authorization, "date": date, "host": host}
    return "ws://" + host + path + "?" + urlencode(params)

def build_http_url(host, path, api_key, api_secret):
    """生成带鉴权参数的 HTTP URL（OCR 等用）。"""
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = (
        "host: " + host + "\n"
        "date: " + date + "\n"
        "POST " + path + " HTTP/1.1"
    )
    signature_sha = base64.b64encode(hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()).decode("utf-8")
    authorization_origin = (
        'api_key="%s", algorithm="%s", headers="%s", signature="%s"'
        % (api_key, "hmac-sha256", "host date request-line", signature_sha)
    )
    authorization = base64.b64encode(
        authorization_origin.encode("utf-8")).decode("utf-8")
    params = {"authorization": authorization, "date": date, "host": host}
    return "https://" + host + path + "?" + urlencode(params)

def build_http_headers(host, path, api_key, api_secret, body_str):
    """构造带 digest 鉴权的请求头（翻译等用）。"""
    date = _httpdate(datetime.utcnow())
    digest = "SHA-256=" + base64.b64encode(
        hashlib.sha256(body_str.encode("utf-8")).digest()
    ).decode("utf-8")
    signature_str = (
        "host: " + host + "\n"
        "date: " + date + "\n"
        "POST " + path + " HTTP/1.1\n"
        "digest: " + digest
    )
    signature = base64.b64encode(hmac.new(
        api_secret.encode("utf-8"),
        signature_str.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()).decode("utf-8")
    # 注意：ITS 的 digest 鉴权 Authorization 是明文（不 base64），
    # 与 OCR/FACE 的 URL 参数 authorization（需 base64）不同。
    authorization = ('api_key="%s", algorithm="%s", '
                     'headers="%s", signature="%s"') % (
        api_key, "hmac-sha256",
        "host date request-line digest", signature)
    return {
        "Authorization": authorization,
        "content-type": "application/json",
        "host": host,
        "date": date,
        "digest": digest,
    }
