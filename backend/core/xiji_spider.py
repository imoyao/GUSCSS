#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/5/7 21:54
import os
import re
import pathlib
from urllib.request import urlopen, Request

from lxml import etree

from backend import settings


class LYLJ:
    """
    烈艳蓝金系列唇膏爬虫
    """
    start_link = settings.DIOR_LYLJ_URL

    def __init__(self):
        pass

    # @staticmethod
    # def get_html(url):
    #     """
    #     爬取一次之后，保存网页到本地
    #     """
    #     content = Request(url, headers=settings.HEADERS)
    #     # content = urllib.request.urlopen(url)  # 发出请求并且接收返回文本对象
    #     response = urlopen(content, timeout=10)
    #     html = response.read()  # 调用read()进行读取
    #     with open('../../_data/xiji/products.html', 'wb+') as f:
    #         f.write(html)
    #     return html

    def current_item_id(self):
        ret = re.split(r"[.-]", self.start_link)
        return ret[-2]

    @staticmethod
    def join_link(link):
        """
        组装成真实的link
        :param link:
        :return:
        """
        return ''.join(['https:', link])

    def mk_dir(self):
        dir_name = '../../_data/lipsticks/Dior/{sn}'.format(sn=self.__class__.__name__.lower())
        if not os.path.exists(dir_name):
            # [Python安全创建目录的方法](https://majing.io/posts/10000007281150)
            pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
        return dir_name

    def load_content(self):
        result = self.get_item_element_tree(self.start_link)
        links = result.xpath('//*[@id="product_spec"]/ul/li/span[2]/ul/li/a/@href')
        item_ids = result.xpath('//*[@id="product_spec"]/ul/li/span[2]/ul/li/a/@rel')
        names = result.xpath('//*[@id="product_spec"]/ul/li/span[2]/ul/li/a/span')

        dir_name = self.mk_dir()

        img_src_list = []  # 对当前页单独处理
        img_src = self.get_image_src(result)
        current_id = self.current_item_id()
        self.save_image(img_src, dir_name, current_id)
        img_src_list.append(img_src)

        current_names = [name.text for name in names]
        links.pop(0)  # 移除第一个script
        print('Start get details……')
        for img_id, link in zip(item_ids, links):
            real_link = self.join_link(link)
            result = self.get_item_element_tree(real_link)
            img_src = self.get_image_src(result)
            self.save_image(img_src, dir_name, img_id)
            img_src_list.append(img_src)

        item_ids.insert(0, current_id)
        return item_ids, current_names, img_src_list

    @staticmethod
    def save_image(img_src, dir_name, image_id):
        fp = '{dirn}/{fn}.{ext}'.format(dirn=dir_name, fn=str(image_id), ext='jpg')
        with open(fp, 'wb') as f:
            img = urlopen(img_src).read()
            f.write(img)
        return 0

    def get_image_src(self, result_obj):
        img_link = result_obj.xpath('//*[@id="op_product_zoom"]/img/@src')
        real_img_src = self.join_link(img_link[0])
        return real_img_src

    @staticmethod
    def get_item_element_tree(item_url):
        """
        给出网页地址，获得网页信息
        :param item_url:
        :return:
        """
        content = Request(item_url, headers=settings.HEADERS)
        response = urlopen(content, timeout=10)
        html = response.read()  # 调用read()进行读取
        result = etree.HTML(html)
        return result


if __name__ == '__main__':
    lylj = LYLJ()
    ret = lylj.load_content()
    print(ret)

    '''
    (['127266', '127267', '127268', '127269', '127270', '127271', '127272'],
     ['#520', '#080', '#740', '#888', '#999金属', '#999滋润', '#999哑光'],
     ['https://img3.xiji.com/images/19/01/5b96671ae769403827ec84b8200805abb36a40a0.jpg?1577773530#w',
      'https://img0.xiji.com/images/19/01/cf3cc958da0bc2b3715b69038ad417ef29523110.jpg?1577773529#w',
      'https://img0.xiji.com/images/19/01/12248f21bf2a429cce01b41fcfd79b232f391e70.jpg?1577773531#w',
      'https://img2.xiji.com/images/19/01/003d9dd19d6612a42b107f427cea2a534c851c42.jpg?1577773531#w',
      'https://img2.xiji.com/images/19/01/fea134055f2050c0a3c9ad992529aa377b0a722f.jpg?1577773532#w',
      'https://img4.xiji.com/images/19/01/6efcdf3646ab405e003d3feefa2d463ac20b9d3a.jpg?1577773534#w',
      'https://img0.xiji.com/images/19/01/ae4fa46845a4db70dc8fe02ed4faa214de12ad1c.jpg?1577773533#w'])
    
    '''
