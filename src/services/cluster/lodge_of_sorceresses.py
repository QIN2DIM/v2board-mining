# -*- coding: utf-8 -*-
# Time       : 2021/12/21 23:59
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: 女术士集会所/女巫小窝
# =============================================
# - intro: 跨越长城 CrossToWorld
# - plan: 2D5GB
# =============================================
ActionCtwCloud = {
    "name": "ActionCtwCloud",
    "register_url": "https://direct.gfwservice.xyz/#/register",
    "hyper_params": {"usr_email": True},
}
# =============================================
# - intro: 云上极速
# - plan: 1D1GB
# =============================================
ActionYunShangCloud = {
    "name": "ActionYunShangCloud",
    "register_url": "https://yunshang.uk/#/register",
    "hyper_params": {},
}
# =============================================
# - intro: 河豚
# - plan: 3H20GB
# =============================================
ActionHeTunCloud = {
    "name": "ActionHeTunCloud",
    "register_url": "https://hetun.online/#/register",
    "hyper_params": {"usr_email": True, "threshold": 0},
    "life_cycle": 3
}
# =============================================
# - intro: 玛瑙云
# - plan: 3D2GB
# =============================================
ActionAgateCloud = {
    "name": "ActionAgateCloud",
    "register_url": "https://manaocloud.xyz/#/register",
    "hyper_params": {"tos": True, "anti_email": True, "api": "https://api.manaocloud.xyz"},
    "life_cycle": 24 * 3
}
# =============================================
# - intro: SNOW
# - plan: 1D1GB
# =============================================
ActionSnowCloud = {
    "name": "ActionSnowCloud",
    "register_url": "https://www.onsnow.net/#/register",
    "hyper_params": {"tos": True},
}
# =============================================
# - intro: TiGR
# - plan: 3D10G
# =============================================
ActionTiGRCloud = {
    "name": "ActionTiGRCloud",
    "register_url": "https://tigr.icu/s/#/register",
    "hyper_params": {"anti_email": True},
    "life_cycle": 24 * 3

}
__entropy__ = [
    # ---------------
    # 无阻碍
    # ---------------
    ActionCtwCloud,  # 2D5GB

    # ---------------
    # 邮箱验证
    # ---------------
    ActionAgateCloud,  # 3D2G
    ActionTiGRCloud,  # 3D10G
]

__pending__ = [
    # low-label
    ActionHeTunCloud,  # 3H20G
    ActionYunShangCloud,  # 1D1G
    ActionSnowCloud,  # 1D1G
]
