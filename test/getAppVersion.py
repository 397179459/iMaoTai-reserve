import re
import requests
from bs4 import BeautifulSoup

# mt_version = "".join(re.findall('new__latest__version">(.*?)</p>',
#                                 requests.get('https://apps.apple.com/cn/app/i%E8%8C%85%E5%8F%B0/id1600482450').text,
#                                 re.S)).replace("版本", '')
# print(mt_version)

# apple商店 i茅台 url
apple_imaotai_url = "https://apps.apple.com/cn/app/i%E8%8C%85%E5%8F%B0/id1600482450"

response = requests.get(apple_imaotai_url)
# 用网页自带的编码反解码，防止中文乱码
response.encoding = response.apparent_encoding
html_text = response.text

# 用bs获取指定的class更稳定，正则可能需要经常改动
soup = BeautifulSoup(html_text, "html.parser")
elements = soup.find_all(class_="whats-new__latest__version")

print(elements)
# 获取p标签内的文本内容
version_text = elements[0].text
print(version_text)
# print(elements.text)
# 这里先把没有直接替换“版本 ”，因为后面不知道空格会不会在，所以先替换文字，再去掉前后空格
version_number = version_text.replace("版本", "").strip()
print(version_number)