import configparser
import os
import config as cf
import process
import privateCrypt

config = configparser.ConfigParser()  # 类实例化

aes_key = privateCrypt.get_aes_key()


def get_credentials_path():
    if cf.CREDENTIALS_PATH is not None:
        return cf.CREDENTIALS_PATH
    else:
        home_path = os.getcwd()
        config_parent_path = os.path.join(home_path, 'myConfig')
        config_path = os.path.join(config_parent_path, 'credentials')
        if not os.path.exists(config_parent_path):
            os.mkdir(config_parent_path)
        return config_path


path = get_credentials_path()
# 这里config需要用encoding，以防跨平台乱码
config.read(path, encoding="utf-8")
sections = config.sections()


def get_location():
    while True:
        location = input(f"请输入精确小区位置，例如[小区名称]，为你自动预约附近的门店:").strip()
        selects = process.select_geo(location)

        a = 0
        for item in selects:
            formatted_address = item['formatted_address']
            province = item['province']
            print(f'{a} : [地区:{province}, 位置:{formatted_address}]')
            a += 1

        while True:
            location_input = input(f"请选择位置序号.重新输入请输入 [r] ,默认选择 [0]:").strip()
            location_input_parse = process.set_default_value(location_input, '0')

            if location_input_parse == 'r':
                print(f'请重新选择')
                continue
            elif not location_input_parse.isdigit() or int(location_input_parse) >= a:
                print(f'请选择正确的序号')
                continue
            else:
                break

        select = selects[int(location_input_parse)]
        formatted_address = select['formatted_address']
        province = select['province']
        print(f'已选择 地区:{province},[{formatted_address}]附近的门店')
        return select


def get_user_yn_confirm(prompt: str, ):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'y':
            return True
        elif user_input in ('n', ''):
            return False
        else:
            print("请输入 'y' 或 'n'")


def get_cfg_location():
    process.init_headers()
    location_select: dict = get_location()
    province = location_select['province']
    city = location_select['city']
    location: str = location_select['location']
    return str(province), str(city), location


def get_cfg_enddate(mobile):
    while True:
        enddate_input = input(
            f"输入 [{mobile}] 截止日期(必须是YYYYMMDD,20230819)。如果不设置截止，默认选择[99999999]：").strip()
        enddate_input_parse = process.set_default_value(enddate_input, '99999999')
        if enddate_input_parse.isdigit() and len(enddate_input_parse) == 8:
            return str(enddate_input_parse)
        else:
            print("输入的日期格式不正确，请重新输入。")


def get_cfg_token_userid(mobile):
    process.get_vcode(mobile)
    code = input(f"输入 [{mobile}] 验证码[XXXXXX]:").strip()
    return process.login(mobile, code)


if __name__ == '__main__':

    while True:
        mobile = input(f"请输入手机号 [12312341234]:").strip()
        encrypt_mobile = privateCrypt.encrypt_aes_ecb(mobile, aes_key)

        if encrypt_mobile in sections:
            print(f'[{mobile}] 已存在，将运行更新程序')
            change_flag = False
            initHeader_flag = False

            if get_user_yn_confirm(f"是否需要修改 [{mobile}] 截止时间，[y/n]，默认不修改[n]:"):
                enddate = get_cfg_enddate(mobile)

                config.set(encrypt_mobile, 'enddate', enddate)

                change_flag = True
                print(f"已更新 [{mobile}] 截止时间")
            else:
                print(f"不修改 [{mobile}] 截止时间")

            if get_user_yn_confirm(f"是否需要修改 [{mobile}] 预约位置，[y/n]，默认不修改[n]:"):
                province, city, location = get_cfg_location()
                initHeader_flag = True

                config.set(encrypt_mobile, 'province', province)
                config.set(encrypt_mobile, 'city', city)
                config.set(encrypt_mobile, 'lat', location.split(',')[1])
                config.set(encrypt_mobile, 'lng', location.split(',')[0])

                change_flag = True
                print(f"已更新 [{mobile}] 预约位置")
            else:
                print(f"不修改 [{mobile}] 预约位置")

            if get_user_yn_confirm(f"是否需要修改 [{mobile}] token和userid，[y/n]，默认不修改[n]:"):
                if not initHeader_flag:
                    process.init_headers()
                token, userid = get_cfg_token_userid(mobile)
                encrypt_userid = privateCrypt.encrypt_aes_ecb(str(userid), aes_key)

                config.set(encrypt_mobile, 'userid', encrypt_userid)
                config.set(encrypt_mobile, 'token', token)

                change_flag = True
                print(f"已更新 [{mobile}] token和userid")
            else:
                print(f"不修改 [{mobile}] token和userid")

            if change_flag:
                config.write(open(path, 'w+', encoding="utf-8"))  # 保存数据
            else:
                print(f" [{mobile}] 配置未修改")

        else:
            print(f'[{mobile}] 不存在，将运行新增程序')
            config.add_section(encrypt_mobile)  # 首先添加一个新的section

            # 为了增加辨识度，这里做了隐私处理，不参与任何业务逻辑
            hide_mobile = mobile.replace(mobile[3:7], '****')

            province, city, location = get_cfg_location()

            enddate = get_cfg_enddate(mobile)

            token, userid = get_cfg_token_userid(mobile)
            encrypt_userid = privateCrypt.encrypt_aes_ecb(str(userid), aes_key)

            config.set(encrypt_mobile, 'hidemobile', hide_mobile)
            config.set(encrypt_mobile, 'enddate', enddate)
            config.set(encrypt_mobile, 'province', province)
            config.set(encrypt_mobile, 'city', city)
            config.set(encrypt_mobile, 'lat', location.split(',')[1])
            config.set(encrypt_mobile, 'lng', location.split(',')[0])
            config.set(encrypt_mobile, 'userid', encrypt_userid)
            # 因为加密了手机号和Userid，所以token就不做加密了
            config.set(encrypt_mobile, 'token', str(token))

            config.write(open(path, 'w+', encoding="utf-8"))  # 保存数据

        if not get_user_yn_confirm(f"是否继续添加账号[y/n]:"):
            print(f'no more,tks')
            break
        print(f'One More Thing')

    print(f'账号配置已完成，谢谢使用')
