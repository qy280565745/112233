# iflytek_kit：讯飞语音合成和星火大模型

这个文件夹已经写好，不要改。语音伙伴用到它的两个函数：

| 函数 | 做什么 | 谁在用 |
| --- | --- | --- |
| `tts_say(text, save_path=..., voice=...)` | 用 voice 这种声线把文字念出来，存成声音文件 | services.py 的 speak |
| `spark_chat(prompt)` | 把一段提示词交给星火大模型，得到一句回复 | ai_lab.py 的 ai_reply |

## 钥匙写在哪

钥匙写在工程根目录的 `.env` 里，也就是 app.py 所在的那个文件夹。把 `.env.example` 复制一份，改名为 `.env`，在等号右边填上讯飞开放平台控制台里的值：语音合成三项、星火三项。APIKey 和 APISecret 别填反。

```
IFLYTEK_TTS_APPID=
IFLYTEK_TTS_API_KEY=
IFLYTEK_TTS_API_SECRET=
IFLYTEK_SPARK_APPID=
IFLYTEK_SPARK_API_KEY=
IFLYTEK_SPARK_API_SECRET=
```

没有填钥匙时，页面照样能聊：念出来的是一小段演示声音，✨AI 模式的回话换成伙伴的口癖。

## 真的连讯飞时

要先装两个库：`pip install websocket-client requests`。
