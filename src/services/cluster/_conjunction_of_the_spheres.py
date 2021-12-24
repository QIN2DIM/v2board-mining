# -*- coding: utf-8 -*-
# Time       : 2021/12/21 23:59
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: 天球交汇
import json.decoder
import random
import time
from string import printable

from cloudscraper import create_scraper
from cloudscraper.exceptions import CloudflareChallengeError
from requests.exceptions import (
    SSLError,
    HTTPError,
    ConnectionError,
    Timeout,
    RequestException
)
from selenium.common.exceptions import (
    SessionNotCreatedException,
    WebDriverException,
    TimeoutException,
    ElementNotInteractableException
)
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from services.middleware.subscribe_io import SubscribeManager
from services.settings import logger
from services.utils import ToolBox, SubscribeParser
from services.utils import apis_get_email_context, apis_get_verification_code


class BaseAction:
    """采集器底层驱动"""

    def __init__(
            self,
            atomic: dict,
            chromedriver_path: str = None,
            silence: bool = None,
    ):
        """

        :param atomic:
        :param chromedriver_path:
        :param silence:
        """
        """
        TODO [√]驱动参数
        ---------------------
        """
        self.chromedriver_path = "chromedriver" if chromedriver_path is None else chromedriver_path
        self.silence = True if silence is None else silence

        """
        TODO [√]Atomic原子实例
        ---------------------
        hyper_params    |原子实例超级参数
        beat_dance      |集群节拍超级参数
        """
        self.atomic: dict = atomic

        # 默认参数
        self.register_url = self.atomic["register_url"]
        self.action_name = self.atomic.get("name", "BaseAction")
        self.life_cycle = self.atomic.get("life_cycle", 24)
        self.email_domain = self.atomic.get("email_domain", "@gmail.com")
        self.username, self.password, self.email = "", "", ""

        # 超级参数
        self.hyper_params = {
            # 注册阶段
            "usr_email": False,
            "tos": False,
            # 对抗阶段
            "anti_email": False,
            "anti_reCAPTCHA": False,
            "anti_GeeTest": False,
            "anti_Cloudflare": False,
            # 延拓阶段
            "synergy": False,
            # 缓存阶段
            "threshold": 3,
        }
        self.hyper_params.update(self.atomic.get("hyper_params", {}))
        self.beat_dance = self.hyper_params.get("beat_dance", 0)

        self.tos = bool(self.hyper_params["tos"])
        self.usr_email = bool(self.hyper_params["usr_email"])
        self.synergy_mode = bool(self.hyper_params["synergy"])
        self.anti_email = bool(self.hyper_params["anti_email"])
        self.anti_recaptcha = bool(self.hyper_params["anti_reCAPTCHA"])
        self.anti_cloudflare = bool(self.hyper_params["anti_Cloudflare"])
        self.threshold = self.hyper_params["threshold"]

        self.context_anti_email = {}

        """
        TODO [√]平台对象参数
        ---------------------
        """
        self._API_GET_SUBSCRIBE = self.hyper_params.get("api", self.register_url)
        self._PATH_GET_SUBSCRIBE = "/api/v1/user/getSubscribe"
        self.subscribe_url = ""

        """
        TODO [√]驱动超级参数
        ---------------------
        """
        # 任务超时后实体自我销毁
        self.work_clock_global = time.time()
        self.work_clock_utils = self.work_clock_global
        # 最大容灾阈值 单位秒
        self.work_clock_max_wait = 230 if self.anti_email else 120

    def _is_timeout(self):
        if self.work_clock_utils - self.work_clock_global > self.work_clock_max_wait:
            return True
        return False

    def waiting_to_load(self, api):
        """
        register --> dashboard

        :param api:
        :return:
        """
        url = ToolBox.reset_url(url=self._API_GET_SUBSCRIBE, path=self._PATH_GET_SUBSCRIBE)

        time.sleep(0.5)
        for _ in range(45):
            api.get(url)
            if self._is_timeout():
                raise TimeoutException
            if api.current_url != self.register_url:
                break
            time.sleep(0.2)

    def set_chrome_options(self, external: bool = False, options: ChromeOptions = None):
        options = ChromeOptions() if options is None else options
        options.add_argument("user-agent='{}'".format(ToolBox.fake_user_agent()))

        if self.silence is True:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("blink-settings=imagesEnabled=false")
        options.add_argument('--no-sandbox')
        options.add_argument("--lang=zh-CN")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-javascript')
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if not external:
            try:
                return Chrome(options=options, executable_path=self.chromedriver_path)
            except SessionNotCreatedException as e:
                logger.critical(
                    f"<{self.action_name}> 任務核心無法啓動：ChromeDriver 與 Chrome 版本不匹配。 "
                    f"請審核您的 Chrome 版本號并於 http://npm.taobao.org/mirrors/chromedriver/ 拉取對應的驅動鏡像"
                    f"-- {e}"
                )
            except (PermissionError, WebDriverException):
                logger.critical("The `chromedriver` executable may have wrong permissions.")
        else:
            return options

    def generate_account(self, api):
        username = "".join(
            [random.choice(printable[: printable.index("!")]) for _ in range(9)]
        )
        password = "".join(
            [random.choice(printable[: printable.index(" ")]) for _ in range(15)]
        )

        if not self.anti_email:
            if not self.usr_email:
                email = username
            else:
                email = username + self.email_domain
        else:
            email = self.utils_anti_email(api, method="email")
        return username, password, email

    def utils_anti_email(self, api: Chrome, method="email") -> str:
        if method == "email":
            self.context_anti_email = apis_get_email_context(
                api=api,
                main_handle=api.current_window_handle,
            )
            return self.context_anti_email["email"]
        if method == "code":
            api.find_elements(By.XPATH, "//button[@type='submit']")[0].click()
            email_code = apis_get_verification_code(
                api=api,
                link=self.context_anti_email["link"],
                main_handle=api.current_window_handle,
                collaborate_tab=self.context_anti_email["handle"],
            )
            api.find_element(By.XPATH, "//input[@placeholder='邮箱验证码']").send_keys(email_code)

            return email_code

    def sign_in(self):
        pass

    def sign_up(self, api):
        # 灌入实体内脏数据
        self.username, self.password, self.email = self.generate_account(api)

        # 加入全局超时判断的 register 生命周期轮询
        while True:
            # 超时销毁
            if self._is_timeout():
                raise TimeoutException

            """
            [√]灌入基础信息
            ---------------------
            """
            time.sleep(0.5 + self.beat_dance)
            try:
                email_field = api.find_element(By.XPATH, "//input[@placeholder='邮箱']")
                password_fields = api.find_elements(By.XPATH, "//input[@placeholder='密码']")
                email_field.clear()
                email_field.send_keys(self.email)
                for element in password_fields:
                    element.clear()
                    element.send_keys(self.password)
            except (ElementNotInteractableException, WebDriverException):
                time.sleep(0.5 + self.beat_dance)
                continue

            # 确认服务条款
            if self.tos:
                api.find_element(By.XPATH, "//input[@type='checkbox']").click()

            """
            [√]对抗模组
            ---------------------
            """
            # 邮箱验证
            if self.anti_email:
                assert self.utils_anti_email(api, method="code")
            # Google reCAPTCHA 人机验证
            # if self.anti_recaptcha:
            #     pass

            """
            [√]提交数据
            ---------------------
            """
            time.sleep(0.5)
            for _ in range(3):
                try:
                    api.find_elements(By.XPATH, "//button[@type='submit']")[-1].click()
                    break
                except (ElementNotInteractableException, WebDriverException):
                    ToolBox.echo(
                        msg=f"正在同步集群节拍 | "
                            f"action={self.action_name} "
                            f"hold={1.5 + self.beat_dance}s "
                            f"session_id={api.session_id} "
                            f"event=`register-pending`",
                        level=2
                    )
                    time.sleep(3 + self.beat_dance)
                    continue
            return True

    def check_in(self):
        pass

    @staticmethod
    def get_html_handle(api, url, wait_seconds: int = 15):
        api.set_page_load_timeout(time_to_wait=wait_seconds)
        api.get(url)

    def check_heartbeat(self, debug: bool = False):
        ToolBox.runtime_report(self.action_name, motive="CHECK")

        url = self.register_url
        scraper = create_scraper()
        try:
            response = scraper.get(url, timeout=5)
            if response.status_code > 400:
                logger.error(f">> Block <{self.action_name}> InstanceStatusException "
                             f"status_code={response.status_code} url={url}")
                return False
            return True
        except (SSLError, HTTPError):
            if debug:
                logger.warning(f">> Block <{self.action_name}> Need to use a proxy to access the site "
                               f"url={url}")
            return True
        except ConnectionError as e:
            logger.error(f">> Block <{self.action_name}> ConnectionError "
                         f"url={url} error={e}")
            return False
        except Timeout as e:
            logger.error(f">> Block <{self.action_name}> ResponseTimeout "
                         f"url={url} error={e}")
            return False
        except RequestException as e:
            logger.error(f">> Block <{self.action_name}> RequestException "
                         f"url={url} error={e}")
            return False

    def get_subscribe(self, api: Chrome):
        """
        获取订阅

        引入健壮工程 + 手动标注数据集，大幅度增强模型的泛化能力
        :param api:
        :return:
        """
        try:
            self.subscribe_url = SubscribeParser.parse_url_from_json(
                url=ToolBox.reset_url(self._API_GET_SUBSCRIBE, path=self._PATH_GET_SUBSCRIBE),
                api_cookie=api.get_cookies()
            )
        except (CloudflareChallengeError, json.decoder.JSONDecodeError):
            context: str = api.find_element(By.XPATH, "//pre").text
            self.subscribe_url = SubscribeParser.parse_url_from_page(context)

        if self.subscribe_url != "":
            logger.debug(ToolBox.runtime_report(
                action_name=self.action_name,
                motive="GET",
                subscribe_url=self.subscribe_url
            ))

    def cache_subscribe(self, sm: SubscribeManager = None):
        if self.subscribe_url == "":
            return

        sm = SubscribeManager() if sm is None else sm

        # 缓存订阅链接
        sm.add(
            subscribe=self.subscribe_url,
            life_cycle=self.life_cycle,
            threshold=self.threshold
        )

        # 更新别名映射
        sm.set_alias(
            alias=self.action_name,
            netloc=ToolBox.reset_url(
                url=self.subscribe_url,
                get_domain=True
            )
        )

        logger.success(ToolBox.runtime_report(
            action_name=self.action_name,
            motive="STORE",
            subscribe_url=self.subscribe_url
        ))


class TheWitcher(BaseAction):
    def __init__(self, atomic: dict, chromedriver_path: str = None, silence: bool = None, ):
        super(TheWitcher, self).__init__(atomic=atomic, chromedriver_path=chromedriver_path, silence=silence)

    def run(self, api=None, synergy: bool = False, sm: SubscribeManager = None):
        """

        :param sm:
        :param api:
        :param synergy:
        :return:
        """
        logger.debug(ToolBox.runtime_report(
            action_name=self.action_name,
            motive="RUN",
            params=self.hyper_params
        ))

        self.get_html_handle(api=api, url=self.register_url, wait_seconds=45 + self.beat_dance)
        self.sign_up(api)

        if not synergy:
            self.waiting_to_load(api)
            self.get_subscribe(api)
            self.cache_subscribe(sm)
