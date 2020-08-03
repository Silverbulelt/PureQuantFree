# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name="purequant",
    version="1.0.0",
    packages=[
        "purequant",
        "purequant.exchange.okex",
        "purequant.exchange.huobi",
    ],
    platforms = "any",
    description="Professional quantitative trading framework.",
    url="https://github.com/eternalranger/PureQuant",
    author="eternal ranger",
    author_email="interstella.ranger2020@gmail.com",
    license="MIT",
    keywords=[
        "purequant", "quant", "framework", "okex", "trade", "btc"
    ],
)
