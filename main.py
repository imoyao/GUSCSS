#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/4/12 21:36
import os
import json

from backend.core import color_parse
from backend import settings


def get_frontend_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND)


def save_file_to_fe(all_info):
    """
    保存信息到前端目录
    :param all_info:
    :return:
    """
    save_fp = get_frontend_path()
    bak_fp = '.'.join([save_fp, 'bak'])
    print(bak_fp, save_fp)
    # os.rename(settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND, bak_fp)
    with open(save_fp, 'w') as jf:
        json.dump(all_info, jf, ensure_ascii=False, indent=2)  # 避免文字转为 unicode
    return 0


if __name__ == '__main__':
    dump_data = True
    pd = color_parse.ParseData()
    all_data = pd.all_in_one(settings.ALL_IN_ONE_INFO, dump_data=dump_data)
    if dump_data:
        ret_code = save_file_to_fe(all_data)
    print('data dump success.')
