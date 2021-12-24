# -*- coding: utf-8 -*-
# Time       : 2021/12/22 16:15
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import ast
from typing import List

from services.middleware.stream_io import RedisClient


class EntropyHeap(RedisClient):
    def __init__(self):
        super(EntropyHeap, self).__init__()

    def update(self, local_entropy: List[dict]):
        self.db.lpush(self.PREFIX_ENTROPY, str(local_entropy))

    def sync(self) -> List[dict]:
        response = self.db.lrange(self.PREFIX_ENTROPY, 0, 1)
        if response:
            remote_entropy = ast.literal_eval(self.db.lrange(self.PREFIX_ENTROPY, 0, 1)[0])
            return remote_entropy

    def is_empty(self) -> bool:
        return not bool(self.db.llen(self.PREFIX_ENTROPY))
