#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/5/10 9:51
from collections import defaultdict
import itertools


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
