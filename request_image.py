#!/usr/bin/env python3
# coding: utf-8

import json
import requests
import os


# def request_image(data):
#     proxies = {
#         "http": "http://127.0.0.1:7890",
#         "https": "http://127.0.0.1:7890",
#     }
#     url = "https://script.google.com/macros/s/AKfycbz8Gu_u3z7nBdfLMFH_p9H1w2mOUEQ0q69Kk0B-Fjp_o4uixySWiMiYW5YUv5LC06-A3w/exec"
#     res = requests.post(
#         url,
#         proxies=proxies,
#         json=data,
#     )
#     print(res.text)


def request_image(path, data):
    import telegram

    chat_id = -1001570498936
    token = os.getenv("yb_chan_bot")
    pp = telegram.utils.request.Request(proxy_url="https://127.0.0.1:7890")
    bot = telegram.Bot(token=token, request=pp)
    # bot.send_message(chat_id=chat_id, text="???")
    with open(path, "rb") as f:
        text = "\n".join([f"*{i}:*  {data[i]}" for i in data])
        bot.send_photo(chat_id, f, caption=text, parse_mode="Markdown")


def request_text(data):
    import telegram

    chat_id = -1001570498936
    token = os.getenv("yb_chan_bot")
    print(token)
    pp = telegram.utils.request.Request(proxy_url="https://127.0.0.1:7890")
    bot = telegram.Bot(token=token, request=pp)
    bot.send_message(chat_id=chat_id, text=data)
    # with open(path, "rb") as f:
    #     text = "\n".join([f"*{i}:*  {data[i]}" for i in data])
    #     bot.send_photo(chat_id, f, caption=text, parse_mode="Markdown")


if __name__ == "__main__":
    # test为true直接返回post值不请求tgbot
    request_text("hello world")
