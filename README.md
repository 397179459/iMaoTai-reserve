
# i茅台预约脚本----GitHub Actions版
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

### 2、(可选)修改config.py，按照你的需求修改相关配置


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

```

### 4、python3 main.py ,执行预约操作
```shell
python3 main.py
```

### 5、配置 Github actions，每日自动预约，省去自己买服务器的成本。

## 请开发者喝咖啡
- 欢迎使用支付宝或微信请我喝咖啡（O.o）

![](resources/imgs/wxqr.png)

![](resources/imgs/zfbqr.jpg)


## 特别感谢
技术思路：https://blog.csdn.net/weixin_47481826/article/details/128893239

初版代码：https://github.com/tianyagogogo/imaotai


