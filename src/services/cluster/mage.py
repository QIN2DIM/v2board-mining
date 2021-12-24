# -*- coding: utf-8 -*-
# Time       : 2021/12/24 11:38
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: 清洗无效订阅

from cloudscraper import create_scraper
from cloudscraper.exceptions import CloudflareChallengeError
from requests.exceptions import (
    SSLError, HTTPError, ProxyError
)

from services.middleware.subscribe_io import SubscribeManager
from services.utils import CoroutineSpeedup
from services.utils import ToolBox


class DecoupleBooster(CoroutineSpeedup):
    def __init__(self, docker=None, debug=False):
        super(DecoupleBooster, self).__init__(docker=docker)

        self.sm = SubscribeManager()
        self.debug = debug

    def preload(self):
        self.docker = self.sm.sync()

    def control_driver(self, url, *args, **kwargs):
        scraper = create_scraper()

        try:
            response = scraper.get(url, timeout=10)
            context = response.text if response else ""
            if not context:
                self.sm.detach(subscribe=url, transfer=False)
                return False
            if self.debug:
                ToolBox.echo(
                    msg=ToolBox.runtime_report(
                        motive="CHECK",
                        action_name="DecoupleBooster",
                        message="Subscribe url is healthy.",
                        url=url,
                    ),
                    level=1
                )
            #         share_links = base64.b64decode(response.text).decode("utf-8").split('\n')
            return True
        except (SSLError, HTTPError, ProxyError):
            self.sm.detach(subscribe=url, transfer=False)
        except CloudflareChallengeError:
            pass


def decouple(debug=False):
    if not ToolBox.check_local_network():
        if debug:
            ToolBox.echo("The local network is abnormal and the decoupler is skipped.", 0)
        return False
    sug = DecoupleBooster(debug=debug)
    sug.preload()
    sug.go()
