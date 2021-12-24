# -*- coding: utf-8 -*-
# Time       : 2021/12/22 9:00
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: 精灵

from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import MaxRetryError

from services.settings import PATH_CHROMEDRIVER
from services.settings import logger
from ._conjunction_of_the_spheres import TheWitcher


class LionCubOfCintra(TheWitcher):
    def __init__(self, atomic: dict, chromedriver_path: str = None, silence: bool = None):
        """

        :param atomic:
        :param chromedriver_path:
        :param silence:
        """
        super(LionCubOfCintra, self).__init__(atomic, chromedriver_path=chromedriver_path, silence=silence)

    def assault(self, api=None, synergy: bool = None, force: bool = False, **kwargs):

        # 心跳检测
        if not force:
            if not self.check_heartbeat():
                return

        # 获取驱动器
        api = self.set_chrome_options() if api is None else api
        if not api:
            return

        # 执行驱动
        try:
            self.run(api, synergy=synergy, sm=kwargs.get("sm"))
        except WebDriverException as e:
            logger.exception(e)
        finally:
            # MaxRetryError
            # --------------
            # 场景：多个句柄争抢驱动权限 且有行为在驱动退出后发生。也即调用了已回收的类的方法。
            # 在 deploy 模式下，调度器可以在外部中断失活实例，此时再进行 api.quit() 则会引起一系列的 urllib3 异常
            try:
                api.quit()
            except MaxRetryError:
                pass


def devil_king_armed(atomic: dict, silence=True, mirror=False):
    """
    Production line for running instances

    :param atomic:
    :param silence:
    :param mirror:  规定在 deploy 中使用 False 在 Scaffold.spawn() 中使用True
    :return:
    """
    cirilla = LionCubOfCintra(
        atomic=atomic,
        silence=silence,
        chromedriver_path=PATH_CHROMEDRIVER
    )
    return cirilla if mirror is False else cirilla.assault
