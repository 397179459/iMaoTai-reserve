import datetime
import logging
import sys

import config
import login
import process
import privateCrypt
from shadow import shadow

DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
TODAY = datetime.date.today().strftime("%Y%m%d")
# utc 时间 小时数+8为北京时间
# HOUR = int(datetime.datetime.utcnow().strftime("%H"))
HOUR = 11
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
                    stream=sys.stdout,
                    datefmt=DATE_FORMAT)

print(r'''
**************************************
    欢迎使用i茅台自动预约工具
    作者GitHub：https://github.com/3 9 7 1 7 9 4 5 9
    vx：L 3 9 7 1 7 9 4 5 9 加好友注明来意
**************************************
''')

process.get_current_session_id()

# 校验配置文件是否存在
configs = login.config
if len(configs.sections()) == 0:
    logging.error("配置文件未找到配置")
    sys.exit(1)

aes_key = privateCrypt.get_aes_key()

s_title = '茅台预约成功！记得下午6点查看预约结果。'
s_content = ""

if HOUR == 1: # 上午9：00~上午9：59
    logging.info(f"当前是北京时间{HOUR + 8}时，开始预约申购...")
elif HOUR >= 10:  # 下午6点以后
    logging.info(f"当前是北京时间{HOUR + 8}时，开始查询申购结果...")


for section in configs.sections():
    if (configs.get(section, 'enddate') != 9) and (TODAY > configs.get(section, 'enddate')):
        continue
    mobile = privateCrypt.decrypt_aes_ecb(section, aes_key)
    mask_mobile = shadow(mobile)
    province = configs.get(section, 'province')
    city = configs.get(section, 'city')
    token = configs.get(section, 'token')
    userId = privateCrypt.decrypt_aes_ecb(configs.get(section, 'userid'), aes_key)
    lat = configs.get(section, 'lat')
    lng = configs.get(section, 'lng')

    p_c_map, source_data = process.get_map(lat=lat, lng=lng)

    process.UserId = userId
    process.TOKEN = token
    process.init_headers(user_id=userId, token=token, lng=lng, lat=lat)
    # 根据配置中，要预约的商品ID，城市 进行自动预约
    try:
        if HOUR == 1: # 上午9：00~上午9：59
            s_content = s_content + "\n"
            for item in config.ITEM_CODES:
                max_shop_id = process.get_location_count(province=province,
                                                         city=city,
                                                         item_code=item,
                                                         p_c_map=p_c_map,
                                                         source_data=source_data,
                                                         lat=lat,
                                                         lng=lng)
                if max_shop_id == '0':
                    continue
                shop_info = source_data.get(str(max_shop_id))
                title = config.ITEM_MAP.get(item)
                shopInfo = f'商品({title}),门店({shop_info["name"]})'
                logging.info(shopInfo)
                reservation_params = process.act_params(max_shop_id, item)
                # 核心预约步骤
                r_success, r_content = process.reservation(reservation_params, mask_mobile)
                # 为了防止漏掉推送异常，所有只要有一个异常，标题就显示失败
                if not r_success:
                    s_title = '！！失败！！茅台预约'
                s_content = s_content + r_content + shopInfo + "\n"
                # 领取小茅运和耐力值
                process.getUserEnergyAward(mask_mobile)
        elif HOUR >= 10: # 下午6点以后
            # 查询申购结果
            check_success, check_content = process.checkReserveResult(mask_mobile)
            if check_success == True:
                s_title = "恭喜！ 茅台申购成功，请尽快付款！"
            else:
                s_title = "很遗憾，茅台申购失败，明天继续加油！"
            s_content = s_content + check_content + "\n"
    except BaseException as e:
        print(e)
        logging.error(e)

# 推送消息
process.send_msg(s_title, s_content)
