#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/4/12 16:48
"""
将json中的数据转化名称由unicode转为汉字
名称转为拼音
"""
import os
import re
import json
from functools import wraps, partial

import yaml
from pypinyin import lazy_pinyin, Style
from backend.libs.zhtools.langconv import Converter

from backend import settings


class ConvertColor:
    """
    see also: https://www.rapidtables.com/convert/color/
    """

    def make_color_id(self, hex_str):
        """
        使用hex色值组装颜色编号
        :param hex_str: str,
        :return: str,
        """
        rgb = []
        if not rgb:
            rgb = self.hex_to_rgb(hex_str)
        assert isinstance(rgb, list)
        color_id = ''.join([str(i) for i in rgb])
        return color_id

    @staticmethod
    def hex_to_rgb(hex_str):
        """
        将颜色的 hex 转化为 rgb
        see also: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        :param hex_str:
        :return:
        """
        assert hex_str.startswith('#')
        h = hex_str.lstrip('#')
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

    @staticmethod
    def rgb_to_cmyk(rgb_seq):
        r, g, b = rgb_seq
        if (r == 0) and (g == 0) and (b == 0):
            # black
            return 0, 0, 0, settings.CMYK_SCALE
        # rgb [0,255] -> cmy [0,1]
        c = 1 - r / 255.
        m = 1 - g / 255.
        y = 1 - b / 255.
        # extract out k [0,1]
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy

        # rescale to the range [0,cmyk_scale]
        return round(c * settings.CMYK_SCALE), round(m * settings.CMYK_SCALE), round(y * settings.CMYK_SCALE), round(
            k * settings.CMYK_SCALE)

    @staticmethod
    def hue_calculate(round1, round2, delta, add_num):
        return (((round1 - round2) / delta) * 60 + add_num) % 360

    def rgb_to_hsv(self, rgb_seq):
        """
        将颜色的rgb序列 转化为hsv值
        :param rgb_seq: Iterable,
        :return: tuple,
        """
        r, g, b = rgb_seq
        r_round = float(r) / 255
        g_round = float(g) / 255
        b_round = float(b) / 255
        max_c = max(r_round, g_round, b_round)
        min_c = min(r_round, g_round, b_round)
        delta = max_c - min_c

        h = None
        if delta == 0:
            h = 0
        elif max_c == r_round:
            h = self.hue_calculate(g_round, b_round, delta, 360)
        elif max_c == g_round:
            h = self.hue_calculate(b_round, r_round, delta, 120)
        elif max_c == b_round:
            h = self.hue_calculate(r_round, g_round, delta, 240)
        if max_c == 0:
            s = 0
        else:
            s = (delta / max_c) * 100
        v = max_c * 100
        return h, s, v


class ParseData:

    @staticmethod
    def get_data_from_json(json_fp):
        """
        从指定的json文件中解析数据
        :param json_fp:str,文件路径
        :return:dict,
        """
        with open(json_fp) as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_data_from_yaml(yaml_fp):
        """
        从指定的yaml文件中解析数据
        :param yaml_fp:文件路径
        :return: dict,
        """
        with open(yaml_fp) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def sugar_data(self, data_info):
        """
        原始数据已经在data中，直接读取并解析
        :param data_info:
        :return:
        """
        sugar = dict()
        fp = data_info.get('data_load_path')
        assert os.path.exists(fp)
        _, f_type = os.path.splitext(fp)
        if f_type == '.json':
            sugar = self.get_data_from_json(fp)
        elif f_type == '.yml':
            sugar = self.get_data_from_yaml(fp)
        return sugar

    def parse_zerosoul(self):
        zs_colors = []
        self_check_list = []
        data = self.sugar_data(settings.CHINESE_COLORS_INFO)

        def make_color_series_list(cus_color_lists, know_color_series=''):
            color_series_lists = []
            compute_color_series = ''
            for _color in cus_color_lists:
                _color_simple_name = _color.get('name')
                _color_hex = _color.get('hex')
                color_desc = _color.get('intro', '')
                color_figure = _color.get('figure', '')
                pinyin_str = ' '.join(lazy_pinyin(_color_simple_name, style=Style.TONE))
                color_tra_name = trans_simple_or_trans(_color_simple_name)
                _color_rgb = converter.hex_to_rgb(_color_hex)
                color_id = converter.make_color_id(_color_hex)
                color_cmyk = converter.rgb_to_cmyk(_color_rgb)

                if not know_color_series:
                    find_color_series.set_color_name(_color_simple_name)
                    compute_color_series = find_color_series(_color_rgb)  # 运算得到的
                _color_series = know_color_series or compute_color_series

                _color_hex = _color_hex.upper() if _color_hex.islower() else _color_hex
                
                color_obj = {
                    'id': color_id,
                    'name': _color_simple_name,
                    'tra_name': color_tra_name,
                    'color_series': _color_series,
                    'pinyin': pinyin_str,
                    'rgb': _color_rgb,
                    'hex': _color_hex,
                    'cmyk': color_cmyk,
                    'desc': color_desc,
                    'figure': color_figure,
                }

                color_series_lists.append(color_obj)
            return color_series_lists

        for color_series_data in data:
            color_series_name = color_series_data.get('name')  # 中文
            # 重新分类
            if color_series_name in settings.COLOR_SERIES_MAP_REVERSE.keys():
                color_series = settings.COLOR_SERIES_MAP_REVERSE.get(color_series_name)  # 英文
                color_lists = color_series_data.get('colors')
                sugar_color_info = make_color_series_list(color_lists, know_color_series=color_series)
                zs_colors.extend(sugar_color_info)
            else:  # 不在里面，则需要自检
                color_lists = color_series_data.get('colors')
                self_check_list.extend(color_lists)

            color_info = make_color_series_list(self_check_list)
            zs_colors.extend(color_info)
        # settings.CHINESE_COLORS_INFO['colors'] = zs_colors
        return zs_colors


# def hue_calculate_org(round1, round2, delta, add_num):
#     return ((round1 - round2) / delta + add_num) * 60
#
#
# def rgb_to_hsv_org(rgb_seq):
#     r, g, b = rgb_seq
#     r_round = float(r) / 255
#     g_round = float(g) / 255
#     b_round = float(b) / 255
#     max_c = max(r_round, g_round, b_round)
#     min_c = min(r_round, g_round, b_round)
#     delta = max_c - min_c
#     h = None
#     if delta == 0:
#         h = 0
#     elif max_c == r_round:
#         h = ((g_round - b_round) / delta % 6) * 60
#
#     elif max_c == g_round:
#         h = hue_calculate_org(b_round, r_round, delta, 2)
#     elif max_c == b_round:
#         h = hue_calculate_org(r_round, g_round, delta, 4)
#     if max_c == 0:
#         s = 0
#     else:
#         s = delta / max_c
#     return h, s, max_c


def update_by_value(v):
    """
    根据 V 值去更新色系数据
    :param v:
    :return:
    """
    if v <= 100 / 3 * 1:
        cs = 'black'
    elif v <= 100 / 3 * 2:
        cs = 'gray'
    else:
        cs = 'white'
    return cs


def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def find_color_series_by_name(name=''):
    """
    装饰器：通过颜色的中文名称利用正则匹配获取颜色名称
    参见《Python Cookbook 中文版》V3 p342 9.5：定义一个属性可由用户修改的装饰器
    我们假定命名是符合人类主观意识的，即：名称比我们的代码更可靠
    因为按照hsv去匹配的时候会有误差，所以我们先通过名称去直接匹配色系，如果名称中没有关键字，我们再使用自己写的规则
    :param name:
    :return:
    """

    def deco(func):
        color_name_char = name

        @wraps(func)
        def wrapper(*args, **kwargs):
            color_series = ''
            if color_name_char:
                re_ret = re.match(settings.REG_COLOR_SERES, color_name_char)
                if re_ret:
                    color_signal = re_ret.group(1)
                    color_series = settings.COLOR_SERIES_MAP_REVERSE.get(color_signal)

            if color_series == '':
                color_series = func(*args, **kwargs)
            return color_series

        @attach_wrapper(wrapper)
        def set_color_name(new_name):
            nonlocal color_name_char
            color_name_char = new_name

        return wrapper

    return deco


converter = ConvertColor()


@find_color_series_by_name(name='')
def find_color_series(rgb_seq):  # TODO:此处是否有更好实现？
    """
    TODO: see also: https://github.com/MisanthropicBit/colorise/blob/master/colorise/color_tools.py
    将rgb转为hsv之后根据h和v寻找色系
    :param rgb_seq:
    :return:
    """
    h, s, v = converter.rgb_to_hsv(rgb_seq)
    cs = None
    if 30 < h <= 90:
        cs = 'yellow'
    elif 90 < h <= 150:
        cs = 'green'
    elif 150 < h <= 210:
        cs = 'cyan'
    elif 210 < h <= 270:
        cs = 'blue'
    elif 270 < h <= 330:
        cs = 'purple'
    elif h > 330 or h <= 30:
        cs = 'red'

    if s < 10:  # 色相太淡时，显示什么颜色主要由亮度来决定
        cs = update_by_value(v)
    assert cs in settings.COLOR_SERIES_MAP
    return cs


def trans_tra_to_simple(tar_str):
    """
    将繁体字转为简体字
    :param tar_str: str,繁体字
    :return: str,简体字
    """

    simple_str = Converter('zh-hans').convert(tar_str)
    return simple_str


def trans_simple_or_trans(in_str, is_simple=True):
    """
    给繁体（必须同时制定is_simple=False），返简体；给简体，返繁体
    :param in_str: str,
    :param is_simple: str,
    :return:
    """
    if is_simple:
        single = 'zh-hant'  # 简to繁
    else:
        single = 'zh-hans'  # 繁to简
    out_str = Converter(single).convert(in_str)
    return out_str


def unify_color_dict(color):
    """
    将颜色统一化
    1. 所有大写key转小写
    2. 字符型 value 返回为解释器读取类型
    :param color:
    :return:
    """
    color_obj = dict()
    for k, v in color.items():
        if isinstance(v, str):
            v = repr(v)
        if k.isupper():
            k = k.lower()

        color_obj[k] = v
    return color_obj


def get_colors_data():
    """
    处理数据并原地更新后返回
    1. 从数据文件中导入数据并转化
    2. 将获取到的json数据中的拼音声调化
    3.hex全部转化为大写
    """

    data_list = get_data_from_json(settings.JSON_LOAD_FP)
    new_color_lists = []
    for color in data_list:
        name = color.get('name')
        hex_str = color.get('hex')
        color_id = make_color_id(hex_str)
        # see also: http://pypinyin.mozillazg.com/zh_CN/master/api.html#pypinyin.lazy_pinyin
        pinyin_str = ' '.join(lazy_pinyin(name, style=Style.TONE))
        color['id'] = color_id
        color['pinyin'] = pinyin_str
        color['hex'] = hex_str.upper()
        j_color_obj = unify_color_dict(color)

        new_color_lists.append(j_color_obj)
        # new_color_lists.append({k.lower(): v for k, v in color.items()})
    id_from_json = [c.get('id') for c in new_color_lists]

    # print(len(id_from_json))
    data_from_yaml = get_data_from_yaml(settings.YAML_LOAD_FP)
    # print(len(trans2dict))
    for color in data_from_yaml:
        hex_str = color.get('hex')
        tra_name = color.get('name')
        color_id = make_color_id(hex_str)
        simple_name = trans_tra_to_simple(tra_name)
        color['id'] = color_id
        color['name'] = simple_name
        if color_id not in id_from_json:  # 去重
            color_obj = unify_color_dict(color)
            new_color_lists.append(color_obj)
    # print(len(new_color_lists))
    return new_color_lists


if __name__ == '__main__':
    # print(get_colors_data())
    import colorsys

    color_list = settings.COLOR_BASE_MAP.values()

    for item in color_list:
        print(find_color_series(item))
        # print(colorsys.rgb_to_hsv(*item))
        # print('rgb_to_hsv:', rgb_to_hsv(item))
        # print('rgb_to_hsv_org:', rgb_to_hsv_org(item))
    print('------------------')
    a = [100, 106, 88]
    print(find_color_series(a))
