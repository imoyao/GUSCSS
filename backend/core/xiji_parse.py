#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/5/8 23:24
import os
import re

from backend.core import img_ocr, xiji_spider
from backend import settings, utils
# from backend.core.img_ocr import time_it

lylj = xiji_spider.LYLJ()


# @time_it
def get_item_detail(dir_p):
    """
    1. 获取图片rgb值
    2. 对数据进行ocr识别,获取描述
    3. 对识别结果进行解析处理
    4. 组装数据
    :param dir_p:
    :return:
    """
    all_li = []
    for root, dirs, files in os.walk(dir_p):
        for f in files:
            fp = os.path.join(root, f)
            fn = os.path.basename(fp)
            only_name = fn.split('.')[0]
            rgb = img_ocr.get_rgb_of_img_load(fp)  # 1
            ocr_text = img_ocr.baidu_ocr.basic_accurate(fp)  # 2

            words_result = ocr_text.get('words_result')  # 3
            ocr_obj = {}
            for index, word in enumerate(words_result):
                if '(' in word.get('words'):
                    subtitle = words_result[index].get('words')
                    re_ret = re.match(settings.REG_LYLJ_SUBTITLE_EXP, subtitle)
                    if re_ret:
                        real_subtitle = re_ret.group(1)
                        ocr_obj['subtile'] = real_subtitle
                    desc_list = words_result[index + 1:]
                    desc = ''.join([desc.get('words') for desc in desc_list])
                    ocr_obj['desc'] = desc

            lipsticks_obj = {  # 4
                'rgb': rgb,
                'id': only_name,
            }
            lipsticks_obj.update(ocr_obj)
            all_li.append(lipsticks_obj)
    return all_li


# @time_it
def get_lylj_series():
    """
    1. 去网络抓取数据
    2. 获取抓取数据的信息
    3. 以id为基准进行合并

    [{'id': '127266', 'name': '#520',
      'src': 'https://img0.xiji.com/images/19/01/5b96671ae769403827ec84b8200805abb36a40a0.jpg?1577773530#w',
      'rgb': (247, 0, 83), 'subtile': '爱情水红恋爱中的粉红', 'desc': '这是一支非常有寓意的口红,520我爱你,表白专属色。这是散发着恋爱中粉红泡泡的颜色,暧昧、热恋,都洋溢在唇间。'},
     {'id': '127267', 'name': '#080',
      'src': 'https://img3.xiji.com/images/19/01/cf3cc958da0bc2b3715b69038ad417ef29523110.jpg?1577773529#w',
      'rgb': (220, 2, 3), 'subtile': '微笑正红春晚同款色', 'desc': '这款也是正红偏橘的色调,红多橘少,像是血橙的颜色,清新诱人,更适合日常使用。滋润质地,对唇部非常友好。'},
     {'id': '127268', 'name': '#740',
      'src': 'https://img3.xiji.com/images/19/01/12248f21bf2a429cce01b41fcfd79b232f391e70.jpg?1577773531#w',
      'rgb': (181, 46, 24), 'subtile': '脏橘色南瓜色百搭', 'desc': '网红人气爆款,实力显白,送人送礼佳品,这支口红真的是人见人爱,厚涂也可以hold住!'},
     {'id': '127269', 'name': '#888',
      'src': 'https://img1.xiji.com/images/19/01/003d9dd19d6612a42b107f427cea2a534c851c42.jpg?1577773531#w',
      'rgb': (220, 29, 36), 'subtile': '火焰开运色', 'desc': '888发发发,让人想到热烈的火焰,红红火火。如果觉得正红太艳丽大可选择这款,正红偏橘,非常显白有活力。'},
     {'id': '127270', 'name': '#999金属',
      'src': 'https://img4.xiji.com/images/19/01/fea134055f2050c0a3c9ad992529aa377b0a722f.jpg?1577773532#w',
      'rgb': (168, 15, 9), 'subtile': '人鱼姬正红', 'desc': '已经有999的小仙女一定不能错过这款金属光正红,偏光的微闪人鱼姬色在阳光下不灵不灵的,非常富有层次感。'},
     {'id': '127271', 'name': '#999滋润',
      'src': 'https://img0.xiji.com/images/19/01/6efcdf3646ab405e003d3feefa2d463ac20b9d3a.jpg?1577773534#w',
      'rgb': (201, 2, 5), 'subtile': '经典正红色', 'desc': '颜色最纯正的一款正红色,不挑肤色,喜庆特别显气质。嘴唇状态不好的小仙女一定要选这款,能让唇妆看起来更美腻~'},
     {'id': '127272', 'name': '#999哑光',
      'src': 'https://img1.xiji.com/images/19/01/ae4fa46845a4db70dc8fe02ed4faa214de12ad1c.jpg?1577773533#w',
      'rgb': (190, 18, 14), 'subtile': '经典正红色', 'desc': '李佳琦墙裂推荐的一个色号,每个女人都必须拥有,涂上气场两米八!哑光质地,不偏橘也不偏玫,厚涂薄涂都美到爆炸!'}]
    :return:list,
    """

    lylj = xiji_spider.LYLJ()
    ids, names, srcs = lylj.load_content()
    print('Get data from network success!')
    info = []
    for item_id, name, src in zip(ids, names, srcs):
        info.append({'id': item_id, 'name': name, 'src': src})

    item_detail = get_item_detail(settings.LYLJ_IMG_DIR)

    lylj_infos = utils.merge_iterables_of_dict('id', info, item_detail)
    return lylj_infos


if __name__ == '__main__':
    # ret = get_item_detail(settings.LYLJ_IMG_DIR)
    ret = get_lylj_series()
    print(ret)
