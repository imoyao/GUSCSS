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


def main(dump_data=settings.SHOULD_I_DUMP_RESULT_TO_FILE
         , group_data=settings.SHOULD_I_GROUP_DATA):
    pd = color_parse.ParseData()
    all_data = pd.all_in_one(settings.ALL_IN_ONE_INFO, group_data=group_data, dump_data=dump_data)
    if dump_data:
        save_file_to_fe(all_data)
    return all_data


if __name__ == '__main__':
    data = main(dump_data=True, group_data=True)
    print(data)
    print('data dump success.')
