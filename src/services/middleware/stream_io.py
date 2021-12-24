# -*- coding: utf-8 -*-
# Time       : 2021/12/22 0:10
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import redis
from redis.exceptions import ConnectionError

from services.settings import REDIS_NODE, logger


class RedisClient:
    def __init__(
            self,
            host=REDIS_NODE["host"],
            port=REDIS_NODE["port"],
            password=REDIS_NODE["password"],
            db=REDIS_NODE["db"],
            **kwargs,
    ) -> None:
        self.db = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,
            db=db,
            health_check_interval=30,
            **kwargs,
        )

        # 兼容服务
        # self.PREFIX_SUBSCRIBE = "v2rayc_spider:clash"
        self.PREFIX_ALIAS = "v2rss:alias"

        # 特征服务
        self.PREFIX_SUBSCRIBE = "v2board:clash"
        self.PREFIX_API = "v2board:apis:"
        self.PREFIX_DETACH = "v2board:detach"
        self.PREFIX_EMAIL = "v2board:email_code"
        self.PREFIX_ENTROPY = "v2board:entropy"

        self.INSTANCE = "V2RSS云彩姬"

    def ping(self) -> str:
        try:
            if self.db.ping():
                return f"欢迎使用{self.INSTANCE}"
        except ConnectionError as e:
            logger.exception(e)
            return "网络连接异常"

    def __len__(self):
        return self.db.hlen(self.PREFIX_SUBSCRIBE)
