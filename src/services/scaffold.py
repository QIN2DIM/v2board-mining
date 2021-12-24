# -*- coding: utf-8 -*-
# Time       : 2021/12/22 0:12
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:

from gevent import monkey

monkey.patch_all()

from apis.scaffold import (
    entropy,
    runner,
    server
)
from services.middleware.subscribe_io import SubscribeManager
from services.settings import logger, POOL_CAP
from services.utils import ToolBox
from services.cluster import decouple


class Scaffold:
    def __init__(self):
        pass

    @staticmethod
    def ping():
        """
        测试 RedisNode 连接

        :return:
        """
        logger.info(ToolBox.runtime_report(
            motive="PING",
            action_name="ScaffoldPing",
            message=SubscribeManager().ping()
        ))

    @staticmethod
    @logger.catch()
    def decouple():
        """
        清除无效订阅

        :return:
        """
        logger.info(ToolBox.runtime_report(
            motive="DECOUPLE",
            action_name="ScaffoldDecoupler",
            message="Clearing invalid subscriptions..."
        ))
        decouple(debug=True)

    @staticmethod
    @logger.catch()
    def overdue():
        """
        清除过期订阅

        :return:
        """
        try:
            pool_len = SubscribeManager().refresh()
            logger.debug(ToolBox.runtime_report(
                motive="OVERDUE",
                action_name="RemotePool | SpawnRhythm",
                message="pool_status[{}/{}]".format(pool_len, POOL_CAP)
            ))
        except ConnectionError:
            pass

    @staticmethod
    def entropy(update: bool = False, remote: bool = False, check: bool = False):
        """
        采集队列的命令行管理工具。

        Usage: python main.py entropy
        ______________________________________________________________________
        or: python main.py entropy --remote 输出 ``远程执行队列`` 的摘要信息
        or: python main.py entropy --update 将 ``本地执行队列`` 辐射至远端
        or: python main.py entropy --check 检查 ``本地执行队列`` 的健康状态

        :param check:
        :param remote:
        :param update:
        :return:
        """
        if not check:
            entropy.preview(remote=remote)
        if update:
            entropy.update()
        if check:
            entropy.check()

    @staticmethod
    @logger.catch()
    def pool():
        """
        获取订阅的活跃状态

        :return:
        """
        ToolBox.echo(str(SubscribeManager().get_pool_status()), 1)

    @staticmethod
    @logger.catch()
    def spawn(
            silence: bool = True,
            power: int = None,
            remote: bool = False,
            safe: bool = False,
    ):
        """
        并发执行本机所有采集器任务，每个采集器实体启动一次，并发数取决于本机硬件条件。

        Usage: python main.py spawn
        ______________________________________________________________________
        or: python main.py spawn --power=4          |指定并发数
        or: python main.py spawn --remote           |读取远程队列的运行实例
        or: python main.py spawn --safe             |安全启动，过滤掉需要人机验证的任务

        :param safe: 安全启动，过滤掉需要人机验证的实例
        :param silence:静默启动
        :param power:指定并发数
        :param remote:将订阅源标记为 ``远程队列``
        :return:
        """
        runner.spawn(
            silence=silence,
            power=power,
            join=False,
            remote=remote,
            safe=safe
        )

    @staticmethod
    def deploy(collector: bool = None, decoupler: bool = None):
        """
        部署定时任务

        Usage: python main.py deploy
        ______________________________________________________________________
        or: python main.py --collector=False         |强制关闭采集器
        or: python main.py --collector               |强制开启采集器
        or: python main.py --collector --decoupler   |强制开启采集器和订阅解耦器

        >> 默认不使用命令行参数，但若使用参数启动项目，命令行参数的优先级高于配置文件
        >> 初次部署需要先运行 ``python main.py entropy --update`` 初始化远程队列

        :param collector:强制开启/关闭采集器
        :param decoupler:强制开启/关闭订阅解耦器
        :return:
        """
        ss = server.SystemService(
            enable_scheduler=True,
            collector=collector,
            decoupler=decoupler
        )
        ss.startup()

    @staticmethod
    def router():
        raise ImportWarning
