import datetime
import json
import math
import os
import random
import re
import time
import config
from encrypt import Encrypt
import requests
import hashlib
import logging
import hmac
import urllib
import base64
import urllib.parse

AES_KEY = 'qbhajinldepmucsonaaaccgypwuvcjaa'
AES_IV = '2018534749963515'
SALT = '2af72f100c356273d46284f6fd1dfc08'

CURRENT_TIME = str(int(time.time() * 1000))
headers = {}

'''
# 获取茅台APP的版本号，暂时没找到接口，采用爬虫曲线救国
# 用bs获取指定的class更稳定，之前的正则可能需要经常改动
def get_mt_version():
    # apple商店 i茅台 url
    apple_imaotai_url = "https://apps.apple.com/cn/app/i%E8%8C%85%E5%8F%B0/id1600482450"
    response = requests.get(apple_imaotai_url)
    # 用网页自带的编码反解码，防止中文乱码
    response.encoding = response.apparent_encoding
    html_text = response.text
    soup = BeautifulSoup(html_text, "html.parser")
    elements = soup.find_all(class_="whats-new__latest__version")
    # 获取p标签内的文本内容
    version_text = elements[0].text
    # 这里先把没有直接替换“版本 ”，因为后面不知道空格会不会在，所以先替换文字，再去掉前后空格
    latest_mt_version = version_text.replace("版本", "").strip()
    return latest_mt_version


mt_version = get_mt_version()
'''
# 通过ios应用商店的api获取最新版本
mt_version = json.loads(requests.get('https://itunes.apple.com/cn/lookup?id=1600482450').text)['results'][0]['version']


header_context = f'''
MT-Lat: 28.499562
MT-K: 1675213490331
MT-Lng: 102.182324
Host: app.moutai519.com.cn
MT-User-Tag: 0
Accept: */*
MT-Network-Type: WIFI
MT-Token: 1
MT-Team-ID: 
MT-Info: 028e7f96f6369cafe1d105579c5b9377
MT-Device-ID: 2F2075D0-B66C-4287-A903-DBFF6358342A
MT-Bundle-ID: com.moutai.mall
Accept-Language: en-CN;q=1, zh-Hans-CN;q=0.9
MT-Request-ID: 167560018873318465
MT-APP-Version: 1.3.7
User-Agent: iOS;16.3;Apple;?unrecognized?
MT-R: clips_OlU6TmFRag5rCXwbNAQ/Tz1SKlN8THcecBp/HGhHdw==
Content-Length: 93
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: application/json
userId: 2
'''


# 初始化请求头
def init_headers(user_id: str = '1', token: str = '2', lat: str = '29.83826', lng: str = '119.74375'):
    for k in header_context.strip().split("\n"):
        temp_l = k.split(': ')
        dict.update(headers, {temp_l[0]: temp_l[1]})
    dict.update(headers, {"userId": user_id})
    dict.update(headers, {"MT-Token": token})
    dict.update(headers, {"MT-Lat": lat})
    dict.update(headers, {"MT-Lng": lng})
    dict.update(headers, {"MT-APP-Version": mt_version})


def signature(data: dict):
    keys = sorted(data.keys())
    temp_v = ''
    for item in keys:
        temp_v += data[item]
    text = SALT + temp_v + CURRENT_TIME
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf8'))
    md5 = hl.hexdigest()
    return md5


# 获取登录手机验证码
def get_vcode(mobile: str):
    params = {'mobile': mobile}
    md5 = signature(params)
    dict.update(params, {'md5': md5, "timestamp": CURRENT_TIME, 'MT-APP-Version': mt_version})
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/user/register/vcode", json=params,
                              headers=headers)
    if responses.status_code != 200:
        logging.info(
            f'get v_code : params : {params}, response code : {responses.status_code}, response body : {responses.text}')


# 执行登录操作
def login(mobile: str, v_code: str):
    params = {'mobile': mobile, 'vCode': v_code, 'ydToken': '', 'ydLogId': ''}
    md5 = signature(params)
    dict.update(params, {'md5': md5, "timestamp": CURRENT_TIME, 'MT-APP-Version': mt_version})
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/user/register/login", json=params,
                              headers=headers)
    if responses.status_code != 200:
        logging.info(
            f'login : params : {params}, response code : {responses.status_code}, response body : {responses.text}')
    dict.update(headers, {'MT-Token': responses.json()['data']['token']})
    dict.update(headers, {'userId': responses.json()['data']['userId']})
    return responses.json()['data']['token'], responses.json()['data']['userId']


# 获取当日的session id
def get_current_session_id():
    # print("===============get_current_session_id")
    day_time = int(time.mktime(datetime.date.today().timetuple())) * 1000
    my_url = f"https://static.moutai519.com.cn/mt-backend/xhr/front/mall/index/session/get/{day_time}"
    # print(my_url)
    responses = requests.get(my_url)
    # print(responses.json())
    if responses.status_code != 200:
        logging.warning(
            f'get_current_session_id : params : {day_time}, response code : {responses.status_code}, response body : {responses.text}')
    current_session_id = responses.json()['data']['sessionId']
    dict.update(headers, {'current_session_id': str(current_session_id)})


# 获取最近或者出货量最大的店铺
def get_location_count(province: str,
                       city: str,
                       item_code: str,
                       p_c_map: dict,
                       source_data: dict,
                       lat: str = '29.83826',
                       lng: str = '102.182324'):
    day_time = int(time.mktime(datetime.date.today().timetuple())) * 1000
    session_id = headers['current_session_id']
    responses = requests.get(
        f"https://static.moutai519.com.cn/mt-backend/xhr/front/mall/shop/list/slim/v3/{session_id}/{province}/{item_code}/{day_time}")
    if responses.status_code != 200:
        logging.warning(
            f'get_location_count : params : {day_time}, response code : {responses.status_code}, response body : {responses.text}')
    shops = responses.json()['data']['shops']

    if config.RESERVE_RULE == 0:
        return distance_shop(city, item_code, p_c_map, province, shops, source_data, lat, lng)

    if config.RESERVE_RULE == 1:
        return max_shop(city, item_code, p_c_map, province, shops)


# 获取距离最近的店铺
def distance_shop(city,
                  item_code,
                  p_c_map,
                  province,
                  shops,
                  source_data,
                  lat: str = '28.499562',
                  lng: str = '102.182324'):
    # shop_ids = p_c_map[province][city]
    temp_list = []
    for shop in shops:
        shopId = shop['shopId']
        items = shop['items']
        item_ids = [i['itemId'] for i in items]
        # if shopId not in shop_ids:
        #     continue
        if str(item_code) not in item_ids:
            continue
        shop_info = source_data.get(shopId)
        # d = geodesic((lat, lng), (shop_info['lat'], shop_info['lng'])).km
        d = math.sqrt((float(lat) - shop_info['lat']) ** 2 + (float(lng) - shop_info['lng']) ** 2)
        # print(f"距离：{d}")
        temp_list.append((d, shopId))

    # sorted(a,key=lambda x:x[0])
    temp_list = sorted(temp_list, key=lambda x: x[0])
    # logging.info(f"所有门店距离:{temp_list}")
    if len(temp_list) > 0:
        return temp_list[0][1]
    else:
        return '0'


# 获取出货量最大的店铺
def max_shop(city, item_code, p_c_map, province, shops):
    max_count = 0
    max_shop_id = '0'
    shop_ids = p_c_map[province][city]
    for shop in shops:
        shopId = shop['shopId']
        items = shop['items']

        if shopId not in shop_ids:
            continue
        for item in items:
            if item['itemId'] != str(item_code):
                continue
            if item['inventory'] > max_count:
                max_count = item['inventory']
                max_shop_id = shopId
    logging.debug(f'item code {item_code}, max shop id : {max_shop_id}, max count : {max_count}')
    return max_shop_id


encrypt = Encrypt(key=AES_KEY, iv=AES_IV)


def act_params(shop_id: str, item_id: str):
    # {
    #     "actParam": "a/v0XjWK/a/a+ZyaSlKKZViJHuh8tLw==",
    #     "itemInfoList": [
    #         {
    #             "count": 1,
    #             "itemId": "2478"
    #         }
    #     ],
    #     "shopId": "151510100019",
    #     "sessionId": 508
    # }
    session_id = headers['current_session_id']
    userId = headers['userId']
    params = {"itemInfoList": [{"count": 1, "itemId": item_id}],
              "sessionId": int(session_id),
              "userId": userId,
              "shopId": shop_id
              }
    s = json.dumps(params)
    act = encrypt.aes_encrypt(s)
    params.update({"actParam": act})
    return params


# 消息推送
def send_msg(title, content):
    if config.MT_PUSHPLUS_KEY is not None:
        send_push_msg(title, content)
    elif config.MT_DINGTALK_ACCESS_TOKEN is not None and config.MT_DINGTALK_SECRET is not None:
        send_dingtalk_msg(title, content)

# push 消息发送
def send_push_msg(title, content):
    url = 'http://www.pushplus.plus/send'
    r = requests.get(url, params={'token': config.MT_PUSHPLUS_KEY,
                                  'title': title,
                                  'content': content})
    logging.info(f'通知推送结果：{r.status_code, r.text}')

# 钉钉 消息推送
def send_dingtalk_msg(title, content):
    if len(title) == 0 and len(content) == 0:
        return

    timestamp = str(round(time.time() * 1000))
    secret_enc = config.MT_DINGTALK_SECRET.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, config.MT_DINGTALK_SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        "access_token": config.MT_DINGTALK_ACCESS_TOKEN,
        "timestamp": timestamp,
        "sign": sign
    }
    msg_content = {
        "msgtype": "text",
        "text": {
            "content": "%s\n%s"%(title, content)
        }
    }
    response = requests.post("https://oapi.dingtalk.com/robot/send", headers=headers, params=params, json=content)
    logging.info("Dingtalk发送消息状态码：{}".format(response.status_code))


# 核心代码，执行预约
def reservation(params: dict, mobile: str):
    params.pop('userId')
    responses = requests.post("https://app.moutai519.com.cn/xhr/front/mall/reservation/add", json=params,
                              headers=headers)
    ret_msg = responses.json()["message"]
    # if responses.status_code == 401:
    #     send_msg('！！失败！！茅台预约', f'[{mobile}],登录token失效，需要重新登录')
    #     raise RuntimeError

    msg = f'【{mobile}】预约结果：code({responses.status_code}),msg({ret_msg}) '
    logging.info(msg)

    # 如果是成功，推送消息简化；失败消息则全量推送
    if responses.status_code == 200:
        r_success = True
        msg = f'【{mobile}】'
    else:
        r_success = False

    return r_success, msg


# 用高德api获取地图信息
def select_geo(i: str):
    # 校验高德api是否配置
    if config.MT_GAODE_KEY is None:
        logging.error("!!!!请配置config.py中AMAP_KEY(高德地图的MapKey)")
        raise ValueError
    resp = requests.get(f"https://restapi.amap.com/v3/geocode/geo?key={config.MT_GAODE_KEY}&output=json&address={i}")
    geocodes: list = resp.json()['geocodes']
    return geocodes


def get_map(lat: str = '28.499562', lng: str = '102.182324'):
    p_c_map = {}
    url = 'https://static.moutai519.com.cn/mt-backend/xhr/front/mall/resource/get'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X)',
        'Referer': 'https://h5.moutai519.com.cn/gux/game/main?appConfig=2_1_2',
        'Client-User-Agent': 'iOS;17.4.1;Apple;iPhone 13 Pro',
        'MT-R': 'clips_OlU6TmFRag5rCXwbNAQ/Tz1SKlN8THcecBp/HGhHdw==',
        'Origin': 'https://h5.moutai519.com.cn',
        'MT-APP-Version': mt_version,
        'MT-Request-ID': f'{int(time.time() * 1000)}{random.randint(1111111, 999999999)}{int(time.time() * 1000)}',
        'Accept-Language': 'zh-CN,zh-Hans;q=1',
        'MT-Device-ID': f'{int(time.time() * 1000)}{random.randint(1111111, 999999999)}{int(time.time() * 1000)}',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'mt-lng': f'{lng}',
        'mt-lat': f'{lat}'
    }
    res = requests.get(url, headers=headers, )
    mtshops = res.json().get('data', {}).get('mtshops_pc', {})
    urls = mtshops.get('url')
    r = requests.get(urls)
    for k, v in dict(r.json()).items():
        provinceName = v.get('provinceName')
        cityName = v.get('cityName')
        if not p_c_map.get(provinceName):
            p_c_map[provinceName] = {}
        if not p_c_map[provinceName].get(cityName, None):
            p_c_map[provinceName][cityName] = [k]
        else:
            p_c_map[provinceName][cityName].append(k)

    return p_c_map, dict(r.json())


# 领取耐力和小茅运
def getUserEnergyAward(mobile: str):
    """
    领取耐力
    """
    cookies = {
        'MT-Device-ID-Wap': headers['MT-Device-ID'],
        'MT-Token-Wap': headers['MT-Token'],
        'YX_SUPPORT_WEBP': '1',
    }
    response = requests.post('https://h5.moutai519.com.cn/game/isolationPage/getUserEnergyAward', cookies=cookies,
                             headers=headers, json={})
    # response.json().get('message') if '无法领取奖励' in response.text else "领取奖励成功"
    logging.info(
        f'领取耐力 : mobile:{mobile} :  response code : {response.status_code}, response body : {response.text}')

#查询预约结果
def checkReserveResult(mobile: str):
    params = {"lastReserveId":"","reservationId":""}
    # 只拉取第一页
    response = requests.get('https://app.moutai519.com.cn/xhr/front/mall/reservation/list/pageOne/queryV2', headers=headers, json={})
    # 拉取历史第一页
    # response = requests.get('https://app.moutai519.com.cn/xhr/front/mall/reservation/list/more/queryV2', headers=headers, json=params)
    check_content = ""
    check_success = False
    if response.status_code == 200:
        resJson = response.json()
        for idx in range(len(config.ITEM_CODES)):
            lastResult = resJson["data"]["reservationItemVOS"][idx]
            itemName = lastResult["itemName"]
            status = lastResult["status"]
            if status == 2:
                check_success = True
                check_content = check_content + f"🎉【{mobile}】 申购【{itemName}】成功！！\n"
            else:
                check_content = check_content + f"😩【{mobile}】 申购【{itemName}】失败！！\n"
    else:
        # 请求失败
        check_content = f"❌【{mobile}】申购结果查询失败，请去App查看结果！"

    return check_success, check_content