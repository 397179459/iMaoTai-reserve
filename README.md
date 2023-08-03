
# i茅台预约脚本
## 原理：
### 1、登录获取验证码
### 2、输入验证码获取TOKEN
### 3、获取当日SESSION ID
### 4、根据配置文件预约CONFIG文件中，所在城市的i茅台商品

## 使用：

### 1、安装依赖
```shell
pip3 install --no-cache-dir -r requirements.txt
```

### 2、(可选)修改config.py 
```python
import os

ITEM_MAP = {
    "10213": "53%vol 500ml贵州茅台酒（癸卯兔年）",
    "10214": "53%vol 375ml×2贵州茅台酒（癸卯兔年）",
    "10056": "53%vol 500ml茅台1935",
    "2478": "53%vol 500ml贵州茅台酒（珍品）"
}

# 需要预约的商品(默认只预约2个兔茅)
########################
ITEM_CODES = ['10213', '10214']

# push plus 微信推送,具体使用参考  https://www.pushplus.plus
# 例如： PUSH_TOKEN = '123456'
########################
# 不填不推送消息，一对一发送
PUSH_TOKEN = os.environ.get("PUSHPLUS_KEY")
########################

# credentials 路径，例如：CREDENTIALS_PATH = /home/user/.imoutai/credentials
# 不配置，使用默认路径，在宿主目录
# 例如： CREDENTIALS_PATH = '/home/user/.imautai/credentials'
########################
CREDENTIALS_PATH = None
########################

# 预约规则配置
########################
# 预约本市出货量最大的门店
MAX_ENABLED = False
# 预约你的位置附近门店
DISTANCE_ENABLED = True
########################


```

### 3、按提示输入 预约位置、手机号、验证码 等，生成的token等 配置文件会保存在 $HOME/.imaotai/credentials, 很长时间不再需要登录。支持多账号
```shell
python3 login.py

请输入你的位置,例如[小区名称],为你预约本市门店商店: 军安家园
0 : [地区:内蒙古自治区,位置:内蒙古自治区赤峰市红山区军安家园]
请选择位置序号,重新输入请输入[-]:0
已选择 地区:北京市,[北京市海淀区上地十街]附近的门店
输入手机号[13812341234]:1861164****
输入 [1861164****] 验证码[1234]:1234
是否继续添加账号[Y/N]:n

```
```shell
mobian@mobian:~/app/imaotai$ cat ~/.imaotai/credentials 
[1850006****]
city = 西安市
token = zF3viZiQyUeYb5i4dxAhcBWguXS5VFYUPS5Di7BdsLs
userid = 106944****
province = 陕西省
lat = 45.042259
lng = 115.344116

[1863637****]
city = 北京市
token = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
userid = 1102514****
province = 北京市
lat = 45.042259
lng = 115.344116

[1861164****]
city = 太原市
token = 6INvrtyGOTdpsvFmiw0I4FoFNDyG-ekt2WFsQsU9nBU
userid = 10677****
province = 山西省
lat = 45.042259
lng = 115.344116
```

### 4、python3 main.py ,执行预约操作
```shell
python3 main.py
```

## 注意:
### 1、可以配置一个定时任务，执行每日自动预约,建议每天多执行2次
### 2、注意服务器的时区是UTC+8,中国区域
```shell
# imaotai
10,40,50 9 * * * root python3 /home/mobian/app/imaotai/main.py >> /var/log/imaotai.log
```
##### 感谢提供的文档：https://blog.csdn.net/weixin_47481826/article/details/128893239

