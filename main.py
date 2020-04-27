#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/4/12 21:36
import os
import json

from backend.core import color_parse
from backend import settings

pd = color_parse.ParseData()


def get_frontend_path(spec_fp=settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND_CHINESE):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(current_dir, spec_fp)
    return fp


def save_file_to_fe(all_info, spec_fp=settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND_CHINESE):
    """
    保存信息到前端目录
    :param all_info:
    :param is_chinese:bool,
    :return:
    """
    save_fp = get_frontend_path(spec_fp=spec_fp)
    bak_fp = '.'.join([save_fp, 'bak'])
    print(bak_fp, save_fp)
    # os.rename(settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND, bak_fp)
    with open(save_fp, 'w') as jf:
        json.dump(all_info, jf, ensure_ascii=False, indent=2)  # 避免文字转为 unicode
    return 0


def nippon_main(dump_data=settings.SHOULD_I_DUMP_RESULT_TO_FILE
                , group_data=settings.SHOULD_I_GROUP_DATA):
    all_data = pd.parse_nippon_color(group_data=group_data, dump_data=dump_data)
    if dump_data:
        save_file_to_fe(all_data, spec_fp=settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND_NIPPON)
    return all_data


def lip_main(dump_data=settings.SHOULD_I_DUMP_RESULT_TO_FILE):
    all_data = pd.parse_lipstick()
    if dump_data:
        save_file_to_fe(all_data, spec_fp=settings.JSON_COLORS_DATA_DUMP_FOR_FRONTEND_LIPSTICKS)
    return all_data


def main(dump_data=settings.SHOULD_I_DUMP_RESULT_TO_FILE
         , group_data=settings.SHOULD_I_GROUP_DATA):
    all_data = pd.all_in_one(settings.ALL_IN_ONE_INFO, group_data=group_data, dump_data=dump_data)
    if dump_data:
        save_file_to_fe(all_data)
    return all_data


if __name__ == '__main__':
    # chinese_data = main(dump_data=True, group_data=True)
    # print(chinese_data)
    # nippon_data = nippon_main(dump_data=True, group_data=True)
    # print(nippon_data)
    lipsticks = lip_main()
    print(lipsticks)
    print('data dump success.')
