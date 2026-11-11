# -*- coding:utf-8 -*-
"""
client.py — 统一读取凭证、判断是否本地演示、按需导入第三方库。
各个模块都从这里读钥匙，再判断是真的调用讯飞，还是用演示结果。
"""
from . import config, mock

def creds(service):
    """读取某个服务的三项钥匙，交回 (appid, api_key, api_secret)。"""
    return config.get_creds(service)

def mock_mode(service, appid=None, api_key=None, api_secret=None):
    """判断该服务是否走本地演示：强制开关或钥匙不齐。"""
    if mock.forced():
        return True
    if appid or api_key or api_secret:
        return not (appid and api_key and api_secret)
    return not config.has_creds(service)

def lazy_import(package, pip_name=None):
    """用到才导入第三方库；没装时给出安装提示。"""
    try:
        return __import__(package)
    except ImportError as e:
        name = pip_name or package
        raise RuntimeError(f"[依赖缺失] 真实调用需要第三方库，请先安装：pip install {name}") from e
