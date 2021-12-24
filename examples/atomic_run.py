# -*- coding: utf-8 -*-
# Time       : 2021/12/22 18:48
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: The Elder Blood is about to be activated!
import services.cluster.lodge_of_sorceresses as los
from services.cluster import devil_king_armed

# The Fighter
ATOMIC = los.ActionYunShangCloud

# 隐藏指纹
INCOGNITO = False


def demo():
    cirilla = devil_king_armed(ATOMIC, silence=True)

    if INCOGNITO is False:
        cirilla.assault(force=True)
    else:
        from undetected_chromedriver.v2 import Chrome
        cirilla.assault(api=Chrome(), force=True)


if __name__ == '__main__':
    demo()
