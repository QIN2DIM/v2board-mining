from os.path import join, dirname

import pytz

from services.utils import ToolBox

path_output = join(dirname(__file__), "config.yaml")
path_sample = join(dirname(__file__), "config-sample.yaml")
config_ = ToolBox.check_sample_yaml(path_output, path_sample)
"""
================================================ ʕ•ﻌ•ʔ ================================================
                            (·▽·)欢迎使用 v2board-mining，请跟随提示合理配置启动参数
================================================ ʕ•ﻌ•ʔ ================================================
[√]强制填写 [※]可选项
"""
# ---------------------------------------------------
# [√]Redis node configuration
# ---------------------------------------------------
REDIS_NODE = config_["REDIS_NODE"]

# ---------------------------------------------------
# [√]Subscription pool capacity
# ---------------------------------------------------
POOL_CAP = config_["POOL_CAP"]

# ---------------------------------------------------
# [√]Scheduled task configuration
# ---------------------------------------------------
SCHEDULER_SETTINGS = config_["scheduler"]

"""
================================================== ʕ•ﻌ•ʔ ==================================================
                        如果您并非 - V2RSS云彩姬 - 项目开发者 请勿修改以下变量的默认参数
================================================== ʕ•ﻌ•ʔ ==================================================

                                            Enjoy it -> ♂ main.py
"""
# 时区
TIME_ZONE_CN = pytz.timezone("Asia/Shanghai")
TIME_ZONE_NY = pytz.timezone("America/New_York")
