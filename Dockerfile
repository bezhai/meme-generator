FROM python:3.10-slim as app

WORKDIR /app

EXPOSE 2233

VOLUME /data

ENV TZ=Asia/Shanghai \
  LC_ALL=zh_CN.UTF-8 \
  LOAD_BUILTIN_MEMES=true \
  MEME_DIRS="[\"/data/memes\"]" \
  MEME_DISABLED_LIST="[]" \
  GIF_MAX_SIZE=10.0 \
  GIF_MAX_FRAMES=100 \
  BAIDU_TRANS_APPID="" \
  BAIDU_TRANS_APIKEY="" \
  LOG_LEVEL="INFO"

# 复制 requirements.txt 文件
COPY ./requirements.txt /app/requirements.txt

# 复制字体文件
COPY ./resources/fonts/* /usr/share/fonts/meme-fonts/

# 安装系统依赖和 Python 包
RUN apt-get update \
  && apt-get install -y --no-install-recommends locales fontconfig fonts-noto-color-emoji gettext \
  && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
  && fc-cache -fv \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 复制应用程序代码
COPY ./meme_generator /app/meme_generator

# 复制配置文件和启动脚本
COPY ./docker/config.toml.template /app/config.toml.template
COPY ./docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 运行应用程序
RUN python -m meme_generator.cli

CMD ["/app/start.sh"]