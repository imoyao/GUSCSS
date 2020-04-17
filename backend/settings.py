#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/4/12 21:52
JSON_LOAD_FP = '_data/Traditional-Chinese-Colors.json'
YAML_LOAD_FP = '_data/colors-source.yml'
NIPPON_COLOR_LOAD_FP = '_data/nippon-color.json'
JSON_DUMP_FP = '_data/colors.json'
YAML_DUMP_FP = '_data/colors.yml'
CMYK_SCALE = 100

CHINESE_COLORS_INFO = {
    'repo': 'https://github.com/zerosoul/chinese-colors',
    'site': ['https://colors.ichuantong.cn/'],
    'data_load_path': '_data/chinese-colors-in.json',
    'data_dump_path': '_data/chinese-colors-out.json'
}

TRADITIONAL_CHINESE_COLORS_INFO = {
    'repo': 'https://github.com/BoxingP/traditional-chinese-colors',
    'site': ['http://boxingp.github.io/traditional-chinese-colors/'],
    'data_load_path': '_data/Traditional-Chinese-Colors-in.json',
    'data_dump_path': 'Traditional-Chinese-Colors-out.json'
}

NIPPON_COLOR_INFO = {
    'repo': 'https://git.coding.net/ssshooter/nippon-color',
    'site': ['https://Traditional-Chinese-Colorss.com/', 'http://boxingp.github.io/traditional-chinese-colors/',
             'https://colors.flinhong.com/jp-colors/'],
    'data_load_path': ['_data/nippon-color-in.json', '_data/jp-colors-in.yml'],
    'data_dump_path': '_data/nippon-color-out.json'
}
# https://www.rapidtables.com/convert/color/rgb-to-hsv.html
COLOR_BASE_MAP = {
    'black': {'hex': '#000000', 'rgb': (0, 0, 0)},
    'gray': {'hex': '#808080', 'rgb': (128, 128, 128)},
    'white': {'hex': '#FFFFFF', 'rgb': (255, 255, 255)},
    'red': {'hex': '#FF0000', 'rgb': (255, 0, 0)},
    'yellow': {'hex': '#FFFF00', 'rgb': (255, 255, 0)},
    'green': {'hex': '#008000', 'rgb': (0, 128, 0)},
    'cyan': {'hex': '#00FFFF', 'rgb': (0, 255, 255)},
    'blue': {'hex': '#0000FF', 'rgb': (0, 0, 255)},
    'purple': {'hex': '#800080', 'rgb': (128, 0, 128)},
}
# 因为黑白我们的算法基本可以识别所以此处不列出
REG_COLOR_SERES = r'\w*([灰|红|黄|绿|青|蓝|紫])\w*'
# 'black', 'gray', 'white', 'red', 'yellow', 'green', 'cyan', 'blue', 'purple'
COLOR_SERIES_MAP = {
    'black': '黑',
    'gray': '灰',
    'white': '白',
    'red': '红',
    'yellow': '黄',
    'green': '绿',
    'cyan': '青',
    'blue': '蓝',
    'purple': '紫'
}

COLOR_SERIES_MAP_REVERSE = {'黑': 'black', '灰': 'gray', '白': 'white', '红': 'red', '黄': 'yellow', '绿': 'green',
                            '青': 'cyan', '蓝': 'blue', '紫': 'purple'}

# 单个数据样例
single_color = {
    'tra_name': '硃砂紅',
    'simple_name': '朱砂红',
    'is_dark': False,
    'id': 123456,
    'rgb': [184, 75, 72],
    'hex': '#ff4c00',
    'pinyin': 'zhū shā',
    'cmyk': [0, 59, 61, 28],
    'desc': '朱砂的颜色，比大红活泼，也称铅朱朱色丹色（在YM对等的情况下，适量减少红色的成分就是该色的色彩系列感觉）'
}
