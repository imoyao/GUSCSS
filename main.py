#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/4/12 21:36
import os
import json

from backend.core import color_parse

from backend import settings


def write_colors():
    _colors_data = color_parse.get_colors_data()
    with open(settings.JSON_DUMP_FP, 'w') as jf:
        json.dump(_colors_data, jf, ensure_ascii=False)  # 避免文字转为 unicode

    if os.path.exists(settings.YAML_DUMP_FP):
        os.remove(settings.YAML_DUMP_FP)

    with open(settings.YAML_DUMP_FP, 'a+') as yf:
        for color in _colors_data:
            color_obj_str = '''- name: {name}
  pinyin: {pinyin}
  hex: {hex}
  rgb: {rgb}
  cmyk: {cmyk}
                
'''.format(**color)
            yf.write(color_obj_str)
    return 0


if __name__ == '__main__':
    pd = color_parse.ParseData()
    colors_data = pd.parse_zerosoul()
    fp = settings.CHINESE_COLORS_INFO.get('data_dump_path')
    with open(fp, 'w') as jf:
        json.dump(colors_data, jf, ensure_ascii=False)  # 避免文字转为 unicode
    print(colors_data)
    print('data dump success.')
