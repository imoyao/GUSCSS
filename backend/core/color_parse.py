#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/4/12 16:48
"""
将json中的数据转化名称由unicode转为汉字
名称转为拼音
"""
import os
import re
from collections import defaultdict
from functools import wraps, partial
import itertools
import json

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

    @staticmethod
    def rgb_to_yuv(rgb_seq):
        r, g, b = rgb_seq
        y = 0.299 * r + 0.587 * g + 0.114 * b
        u = - 0.1687 * r - 0.3313 * g + 0.5 * b + 128
        v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
        return y, u, v


class ParseData:

    def __init__(self):
        pass

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

    @staticmethod
    def dump_data_to_json(yaml_fp, colors_data):  # TODO: no test!
        with open(yaml_fp, 'a+') as yf:
            for color in colors_data:
                color_obj_str = '''- name: {name}
          pinyin: {pinyin}
          hex: {hex}
          rgb: {rgb}
          cmyk: {cmyk}

        '''.format(**color)
                yf.write(color_obj_str)

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

    @staticmethod
    def color_object_maker(color_name, color_hex, color_rgb='', pinyin_str='', color_series='',
                           color_cmyk='', color_desc='', color_figure='', font_color='', is_simple=True):
        """

        组装颜色对象
        :param color_name: str,必须，如果是繁体，则必须将is_simple置False
        :param color_name:
        :param color_hex:
        :param color_rgb:
        :param pinyin_str:
        :param color_series:
        :param color_cmyk:
        :param color_desc:
        :param color_figure:
        :param font_color:
        :param is_simple:
        :return:
        """
        assert color_hex != ''
        color_id = converter.make_color_id(color_hex)
        color_hex = color_hex.upper() if color_hex.islower() else color_hex
        # 简/繁：此处为知道一个求另一个
        if is_simple:  # TODO: 是否可以简化
            color_simple_name = color_name
            color_tra_name = trans_simple_or_trans(color_name, is_simple=is_simple)
        else:
            color_tra_name = color_name
            color_simple_name = trans_simple_or_trans(color_name, is_simple=is_simple)

        if color_rgb == '':
            color_rgb = converter.hex_to_rgb(color_hex)
        if font_color:
            is_bright = font_color == 'dark'
        else:
            _color_hsv = converter.rgb_to_hsv(color_rgb)
            is_bright = is_bright_color_hsv(_color_hsv)
            font_color = 'dark' if is_bright else 'bright'

        if color_cmyk == '':
            color_cmyk = converter.rgb_to_cmyk(color_rgb)

        if color_series == '':
            find_color_series.set_color_name(color_simple_name)
            color_series = find_color_series(color_rgb)  # 运算得到的
        # http://pypinyin.mozillazg.com/zh_CN/master/api.html#pypinyin.lazy_pinyin
        if pinyin_str == '':
            pinyin_str = ' '.join(lazy_pinyin(color_simple_name, style=Style.TONE))
        return {
            'id': color_id,
            'name': color_simple_name,
            'tra_name': color_tra_name,
            'color_series': color_series,
            'pinyin': pinyin_str,
            'font_color': font_color,
            'is_bright': is_bright,
            'rgb': color_rgb,
            'hex': color_hex,
            'cmyk': color_cmyk,
            'desc': color_desc,
            'figure': color_figure,
        }

    def parse_lipstick(self):
        lipstick_data = self.sugar_data(settings.LIPSTICK_INFO)
        brand_list = []
        for brand in lipstick_data.get('brands'):
            series_list = []
            brand_zh_name = brand.get('name','')
            brand_en_name = brand.get('en_name','')
            if not brand_en_name:
                brand_en_name = '_'.join(lazy_pinyin(brand_zh_name))
            series_name = brand.get('series')
            for series in series_name:
                series_name = series.get('name')
                series_en_name = brand.get('en_name', '')
                if not series_en_name:
                    series_en_name = '_'.join(lazy_pinyin(series_name))
                series_lipsticks = series.get('lipsticks')
                lipsticks_lists = []
                for lipstick in series_lipsticks:
                    lipstick_origin_id = lipstick.get('id')
                    lipstick_hex = lipstick.get('color')
                    lipstick_name = lipstick.get('name')
                    lipstick_obj = self.color_object_maker(lipstick_name, lipstick_hex)
                    lipstick_obj.update({'origin_id': lipstick_origin_id})
                    lipsticks_lists.append(lipstick_obj)
                series_dict = {
                    'name': series_name,
                    'letter': series_en_name,
                    'lipsticks': lipsticks_lists,
                }
                series_list.append(series_dict)
            brand_dict = {
                'name': brand_zh_name,
                'letter': brand_en_name,
                'series': series_list
            }

            brand_list.append(brand_dict)
        all_in_one = {
            'brands': brand_list}
        return all_in_one

    def parse_nippon_color(self, group_data=False, dump_data=False, group_by='color_series'):
        nippon_data = self.sugar_data(settings.NIPPON_COLOR_INFO)
        nippor_list = []
        for color in nippon_data:
            color_series = color.get('color_series')
            font_color = color.get('font_color')
            jp_pinyin_str = color.get('color')
            color_hex = ''.join(['#', color.get('rgb')])
            color_name = color.get('name')
            color_rgb = color.get('Drgb')
            color_obj = self.color_object_maker(color_name, color_hex, color_rgb=color_rgb, pinyin_str=jp_pinyin_str,
                                                color_series=color_series, font_color=font_color, is_simple=False)
            nippor_list.append(color_obj)

        jp_list = []
        jp_data = self.sugar_data(settings.FLINHONG_COLORS_INFO)
        for color in jp_data:
            name = color.get('name')
            jp_pinyin_str = color.get('en-name')
            color_hex = color.get('hex')
            color_rgb = color.get('rgb')
            color_cmyk = color.get('cmyk')
            color_obj = self.color_object_maker(name, color_hex, color_rgb=color_rgb, pinyin_str=jp_pinyin_str,
                                                color_cmyk=color_cmyk, is_simple=False)
            jp_list.append(color_obj)
        all_in_one = merge_iterables_of_dict('id', nippor_list, jp_list)
        if dump_data:
            grouped_data = []
            if group_data:  # 此处只在导出前分组，没有对各组数据分别分组
                grouped_data = group_iterables_of_dicts_in_list_further_series(all_in_one, group_by=group_by)
            dump_data_info = all_in_one if not group_data else grouped_data
            self.dump_data_to_file(dump_data_info, settings.FLINHONG_COLORS_INFO)
            settings.FLINHONG_COLORS_INFO['data'] = dump_data_info
            return settings.FLINHONG_COLORS_INFO
        else:
            return all_in_one

    def parse_flinhong(self, setting_obj, dump_data=False):
        data = self.sugar_data(setting_obj)
        fl_colors = []
        for color in data:
            color_hex = color.get('hex')
            color_name = color.get('name')
            pinyin_str = color.get('pinyin')
            color_rgb = color.get('rgb')
            color_cmyk = color.get('cmyk')
            color_obj = self.color_object_maker(color_name, color_hex, color_rgb=color_rgb, pinyin_str=pinyin_str,
                                                color_cmyk=color_cmyk, is_simple=False)
            fl_colors.append(color_obj)
        if dump_data:
            self.dump_data_to_file(fl_colors, setting_obj)
        return fl_colors

    def parse_jizhi(self, setting_obj, dump_data=False):
        """
        :param setting_obj: setting.JIZHI_INFO
        :param dump_data: bool,
        :return:
        """
        _color_list = []
        data = self.sugar_data(setting_obj)
        for _color in data:
            _color_simple_name = _color.get('name')
            _color_rgb = _color.get('RGB')
            color_cmyk = _color.get('CMYK')
            _color_hex = _color.get('hex')

            color_obj = self.color_object_maker(_color_simple_name, _color_hex, color_rgb=_color_rgb,
                                                color_cmyk=color_cmyk)

            _color_list.append(color_obj)
        if dump_data:
            self.dump_data_to_file(_color_list, setting_obj)
        return _color_list

    def parse_cfs_color(self, setting_obj, dump_data=False):
        """
        只取第二个列表并保存
        :param setting_obj:
        :param dump_data:
        :return:
        """
        data = self.sugar_data(setting_obj)
        _, cts = data
        cts_data = cts.get('list', [])
        _color_list = []
        for _color in cts_data:
            _color_simple_name = _color.get('name')
            _color_hex = _color.get('hex')
            color_obj = self.color_object_maker(_color_simple_name, _color_hex)

            _color_list.append(color_obj)
        if dump_data:
            self.dump_data_to_file(_color_list, setting_obj)
        return _color_list

    def parse_zerosoul(self, setting_obj, dump_data=False):
        """
        :param setting_obj: settings.CHINESE_COLORS_INFO
        :param dump_data:
        :return:
        """
        zs_colors = []
        self_check_list = []
        data = self.sugar_data(setting_obj)

        def make_color_series_list(cus_color_lists, know_color_series=''):
            color_series_lists = []
            for _color in cus_color_lists:
                _color_simple_name = _color.get('name')
                _color_hex = _color.get('hex')
                color_desc = _color.get('intro', '')
                color_figure = _color.get('figure', '')

                color_obj = self.color_object_maker(_color_simple_name, _color_hex,
                                                    color_series=know_color_series, color_desc=color_desc,
                                                    color_figure=color_figure)

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
        if dump_data:
            self.dump_data_to_file(zs_colors, setting_obj)
        return zs_colors

    @staticmethod
    def dump_data_to_file(dump_color_data, setting_obj=None, specific_fp=''):
        if setting_obj is None:
            setting_obj = dict()
        fp = setting_obj.get('data_dump_path') if setting_obj else specific_fp
        # 删旧存新
        if os.path.exists(fp):
            os.remove(fp)

        with open(fp, 'w') as jf:
            setting_obj['data'] = dump_color_data
            json.dump(setting_obj, jf, ensure_ascii=False)  # 避免文字转为 unicode
        return 0

    def all_in_one(self, setting_obj, group_data=False, dump_data=False, group_by='color_series'):
        """

        **注意**：setting和函数名必须对应上，不然会解析出错！
        解析数据并导出（dump_data=True）到配置setting中的配置文件中
        :param setting_obj: dict,
        :param dump_data: bool,是否将运算结果数据导出到文件中
        :param group_data: bool,是否分组
        :param group_by: str,分组依据
        :return: list,
        """
        jizhi_data = self.parse_jizhi(settings.JIZHI_INFO, dump_data=dump_data)
        chinese_colors_data = self.parse_zerosoul(settings.CHINESE_COLORS_INFO, dump_data=dump_data)
        colors_data = self.parse_flinhong(settings.FLINHONG_COLORS_INFO, dump_data=dump_data)
        cfs_color_data = self.parse_cfs_color(settings.CFS_COLOR_INFO, dump_data=dump_data)
        # chinese_colors_data  放后面，因为有描述和图片
        all_in_one = merge_iterables_of_dict('id', jizhi_data, colors_data, cfs_color_data, chinese_colors_data)
        # print(type(all_in_one), all_in_one)
        print('before_filter:', len(jizhi_data) + len(chinese_colors_data) + len(colors_data) + len(cfs_color_data))
        print('after_filter:', len(all_in_one))

        if dump_data:
            grouped_data = []
            if group_data:  # 此处只在导出前分组，没有对各组数据分别分组
                grouped_data = group_iterables_of_dicts_in_list_further_series(all_in_one, group_by=group_by)
            dump_data_info = all_in_one if not group_data else grouped_data
            self.dump_data_to_file(dump_data_info, setting_obj)
            setting_obj['data'] = dump_data_info
            return setting_obj
        else:
            return all_in_one


def group_iterables_of_dicts_in_list_further_series(iterables, group_by='color_series'):
    """
    先分组，然后对色系数据进行更新
    :param iterables:
    :param group_by:
    :return:
    """
    row_by_key = defaultdict(list)
    for _item in iterables:
        row_by_key[_item[group_by]].append(_item)

    further_color_series = dict()
    for k, v in row_by_key.items():
        series_info = settings.COLOR_BASE_MAP.get(k)
        series_info.update({'colors': v})
        further_color_series[k] = series_info
    return further_color_series


def group_iterables_of_dicts_in_list(group_key, iterables):
    """
    按照给定key对iter分组 see also:《Python cookbook》V3:1.15
    :param group_key:
    :param iterables:
    :return:
    """
    row_by_key = defaultdict(list)
    for _item in iterables:
        row_by_key[_item[group_key]].append(_item)
    return row_by_key


def merge_iterables_of_dict(shared_key, *iterables):
    """
    see also:[🐍PyTricks | Python 中如何合并一个内字典列表？ | 别院牧志](https://imoyao.github.io/blog/2020-04-19/python-merge-two-list-of-dicts/)
    chinese_colors_data  放前面，因为有描述和图片
    :param shared_key:
    :param iterables:
    :return:
    """
    result = defaultdict(dict)
    for dictionary in itertools.chain.from_iterable(iterables):
        result[dictionary[shared_key]].update(dictionary)
    # for dictionary in result.values():
    #     dictionary.pop(shared_key)
    # return result
    result = list(result.values())  # 保证返回为list，否则：TypeError: Object of type dict_values is not JSON serializable
    return result


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
def find_color_series(rgb_seq):  # TODO:此处是否有更好实现？cmyk去判断是否是100%cmy颜色(黑色不判断)
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


def is_bright_color_hsv(color_hsv_seq):
    """
    判断颜色是否是亮色（则文字为暗色）
    以便在上面显示清晰文字
    (255, 255, 255): True
    (0, 0, 0): False
    :param color_hsv_seq:
    :return:
    """
    _, s, v_val = color_hsv_seq
    return v_val > 50


def is_bright_color_yuv(color_yuv_seq):
    """
    判断颜色是否是亮色（则文字为暗色）
    以便在上面显示清晰文字
    :param color_yuv_seq:
    :return:
    """
    y_val, _, _ = color_yuv_seq
    return y_val >= 192


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


if __name__ == '__main__':

    color_list = settings.COLOR_BASE_MAP.values()

    for item in color_list:
        print(find_color_series(item))
        # import colorsys
        # print(colorsys.rgb_to_hsv(*item))
        # print('rgb_to_hsv:', rgb_to_hsv(item))
        # print('rgb_to_hsv_org:', rgb_to_hsv_org(item))
    print('------------------')
    a = [100, 106, 88]
    print(find_color_series(a))
