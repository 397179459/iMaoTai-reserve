# 基础镜像
FROM python:3.11.0

# 定义时区
ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

# 定义工作目录
WORKDIR /imaotai

# 拷贝工程文件至镜像
COPY . /imaotai

# 执行容器初始化安装
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/* \
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update && apt-get install -y cron
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pip
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
RUN echo "10 9 * * * root cd /imaotai && /usr/local/bin/python /imaotai/main.py >/dev/null 2>&1" >> /etc/crontab

# 运行的命令
CMD ["cron", "-f"]

# 构建镜像命令
# docker build -t imaotai:v1.0 .

# 容器运行命令
# docker run -itd --restart=always --name=imaotai imaotai:v1.0
