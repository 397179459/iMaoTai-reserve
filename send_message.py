import logging

import requests


def send_server_chan(sckey, title, desp):
    """
    server酱推送
    :param sckey: server酱推送的key
    :param title: 标题
    :param desp: 内容
    :return:
    """
    if sckey:
        url = f"https://sctapi.ftqq.com/{sckey}.send"
        data = {"title": title, "desp": desp}
        response = requests.post(url, data=data)
        if response.json()['data']['error'] == 'SUCCESS':
            logging.info('Server酱 Turbo版推送成功')
        else:
            logging.info('Server酱 Turbo版推送失败')
    else:
        logging.warning("server酱 KEY 没有配置,不推送消息")


def send_pushplus(pushplus_key, title, message):
    """
    pushplus 推送
    :param pushplus_key: pushplus的token
    :param title: 标题
    :param message: 内容
    :return:
    """
    if pushplus_key:
        url = "http://www.pushplus.plus/send"
        data = {"token": pushplus_key, "title": title, "content": message}
        response = requests.post(url, data=data)
        if response.json()['code'] == 200:
            logging.info('PushPlus推送成功')
        else:
            logging.info('PushPlus推送失败')
    else:
        logging.warning("PUSHPLUS_KEY 没有配置,不推送消息")
