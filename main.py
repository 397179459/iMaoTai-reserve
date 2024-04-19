import datetime
import logging
import sys

import config
import login
import process
import privateCrypt
from shadow import shadow

# 全局变量
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
TODAY = datetime.date.today().strftime("%Y%m%d")
# utc时间 小时数+8为北京时间
HOUR = int(datetime.datetime.utcnow().strftime("%H"))
detailTimeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
aes_key = privateCrypt.get_aes_key()
s_title = ''
s_content = ''

def main():
    global s_content
    global s_title

    setup_logging()
    logging.info(f'utc HOUR: {HOUR}')
    configs = setup_useData()
    logging.info(f'检查配置文件完成{configs.sections()}')

    if HOUR == 1 or HOUR >= 10:
        logging.info(f'当前utc HOUR:{HOUR},开始处理逻辑')
        handleAllUsers(configs, HOUR)
    else:
        logging.info("当前非预约时段，请检查设备时间")
        s_title = "当前非预约时段，请检查时间!!"
        s_content = ""

    # 发送通知消息
    process.send_msg(s_title, s_content)
    logging.info('<<<< 处理完成，运行结束 >>>>')
    sys.exit(0)

def handleAllUsers(configs,UGCHour):
    for user in configs.sections():
        if (configs.get(user, 'enddate') != 9) and (TODAY > configs.get(user, 'enddate')):
            continue
        mobile = privateCrypt.decrypt_aes_ecb(user, aes_key)
        mask_mobile = shadow(mobile)
        province = configs.get(user, 'province')
        city = configs.get(user, 'city')
        token = configs.get(user, 'token')
        userId = privateCrypt.decrypt_aes_ecb(configs.get(user, 'userid'), aes_key)
        lat = configs.get(user, 'lat')
        lng = configs.get(user, 'lng')
        p_c_map, source_data = process.get_map(lat=lat, lng=lng)
        process.UserId = userId
        process.TOKEN = token
        process.init_headers(user_id=userId, token=token, lng=lng, lat=lat)
        logging.info(f'process 初始化header完成：{process.headers}')
        if UGCHour == 1: # 去预约
            logging.info(f'在预约时段内，去预约【{mask_mobile}】')
            reserve(province, city, p_c_map, source_data, lat, lng, mask_mobile)
        else: # 查询申购结果
            logging.info(f'在查询申购结果时段内，去查询申购结果【{mask_mobile}】')
            check_reserve_result(mask_mobile)
    return

def reserve(province, city,p_c_map,source_data, lat, lng, mask_mobile):
    global s_content
    global s_title
    s_content = s_content + "\n"
    try:
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
            if r_success == True:
                s_title = "茅台预约成功！记得下午6点查看预约结果。"
            else:
                s_title = '！！失败！！茅台预约'
            s_content = s_content + r_content + shopInfo + "\n"
            # 领取小茅运和耐力值
            process.getUserEnergyAward(mask_mobile)
    except BaseException as e:
        logging.error(f'预约运行错误：{e}')
    return

def check_reserve_result(mobile: str):
    global s_content
    global s_title
    try:
        # 查询申购结果
        check_success, check_content = process.checkReserveResult(mobile)
        s_content = s_content + check_content + "\n"
        if check_success == True:
            s_title = "恭喜！ 茅台申购成功，请尽快付款！"
        else:
            s_title = "很遗憾，茅台申购失败，明天继续加油！"
    except BaseException as e:
        logging.error(f'查询结果运行错误：{e}')
    return

def setup_useData():
    process.get_current_session_id()
    # 校验配置文件是否存在
    configs = login.config
    if len(configs.sections()) == 0:
        logging.error("配置文件未找到配置")
        sys.exit(1)
    return configs

def setup_logging():
    log_file_path = 'log/%s.log'%TODAY # 以天分割log
    logging.basicConfig(filename=log_file_path,
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
                        datefmt=DATE_FORMAT)
    logging.info("<<<< 开始运行 >>>>")
    return

if __name__ == "__main__":
    main()
