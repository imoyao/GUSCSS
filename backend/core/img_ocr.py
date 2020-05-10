#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/5/1 22:49
import time
from functools import wraps

from PIL import Image
from backend.libs.baidu_api.aip import AipOcr

from backend import secrets, settings


class BaiduOCR:
    def __init__(self):
        self.client = AipOcr(secrets.APP_ID, secrets.API_KEY, secrets.SECRET_KEY)
        self.options = {"language_type": "CHN_ENG", "detect_direction": "true", "detect_language": "true",
                        "probability": "true"}

    @staticmethod
    def get_file_content(file_path):
        """
        读取图片
        """
        with open(file_path, 'rb') as fp:
            return fp.read()

    def basic_parse(self, fp, set_option=False):
        image = self.get_file_content(fp)
        option = self.options if set_option else None
        ret = self.client.basicGeneral(image, options=option)
        return ret

    def basic_accurate(self, fp, set_option=False):
        image = self.get_file_content(fp)
        option = self.options if set_option else None
        ret = self.client.basicAccurate(image, options=option)
        return ret

    def basic_parse_url(self, url, set_option=False):
        option = self.options if set_option else None
        ret = self.client.basicGeneralUrl(url, options=option)
        return ret

    def main(self, fp):
        ret_data = self.basic_parse(fp)
        return ret_data


baidu_ocr = BaiduOCR()


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time - start_time
        return func.__name__, res, cost_time

    return wrapper


# @time_it
def get_rgb_of_img_getpixel(fp):
    """
    此处说这个方法比下面的慢，测试相反，需要进一步验证：https://www.cnblogs.com/chimeiwangliang/p/7130434.html
    :param fp:
    :return:
    """
    img = Image.open(fp)
    rgb_color = img.getpixel((96, 720))
    return rgb_color


# @time_it
def get_rgb_of_img_load(fp):
    im = Image.open(fp)  # Can be many different formats.
    pix = im.load()
    # return im.size  # Get the width and hight of the image for iterating over
    return pix[96, 720]  # Get the RGBA Value of the a pixel of an image
    # pix[x, y] = value  # Set the RGBA Value of the image (tuple)
    # im.save('alive_parrot.png')  # Save the modified pixels as .png


if __name__ == '__main__':
    # fp = '../../_data/lipsticks/many.png'
    fp = '../../_data/lipsticks/big-jpg.png'
    ''':param
    
    1: {'log_id': 997397551332359778, 'direction': 0, 'words_result_num': 24, 'words_result': [{'words': '01排', 'probability': {'variance': 0.023368, 'average': 0.853212, 'min': 0.640628}}, {'words': '04排', 'probability': {'variance': 0.062432, 'average': 0.81162, 'min': 0.45852}}, {'words': '08', 'probability': {'variance': 0.002019, 'average': 0.946064, 'min': 0.901128}}, {'words': '09', 'probability': {'variance': 0.000805, 'average': 0.951882, 'min': 0.923516}}, {'words': '16', 'probability': {'variance': 0.0, 'average': 0.999542, 'min': 0.999384}}, {'words': 'AN P KAN ROSE FLAMNGO TRUE CORAL SCARLET ROUOE', 'probability': {'variance': 0.047922, 'average': 0.617961, 'min': 0.16106}}, {'words': '10排', 'probability': {'variance': 0.061092, 'average': 0.824526, 'min': 0.474978}}, {'words': '21', 'probability': {'variance': 0.000295, 'average': 0.980994, 'min': 0.963814}}, {'words': '22#', 'probability': {'variance': 3.7e-05, 'average': 0.993604, 'min': 0.985051}}, {'words': '13排', 'probability': {'variance': 0.054925, 'average': 0.815988, 'min': 0.485028}}, {'words': 'CHERRY LUSH VOLET FATALE NA D CORAL', 'probability': {'variance': 0.025493, 'average': 0.680056, 'min': 0.478117}}, {'words': '5', 'probability': {'variance': 0.0, 'average': 0.994346, 'min': 0.994346}}, {'words': '47', 'probability': {'variance': 0.0, 'average': 0.99995, 'min': 0.999927}}, {'words': '49', 'probability': {'variance': 4e-06, 'average': 0.997941, 'min': 0.99594}}, {'words': '15排', 'probability': {'variance': 0.000654, 'average': 0.980801, 'min': 0.944664}}, {'words': '23排', 'probability': {'variance': 0.042638, 'average': 0.852769, 'min': 0.560751}}, {'words': 'SHOWGIRL LLAC NYMPH MSEMAVED WLD ONER BARE PEACH', 'probability': {'variance': 0.019127, 'average': 0.637065, 'min': 0.357038}}, {'words': '35', 'probability': {'variance': 0.0, 'average': 0.999222, 'min': 0.998675}}, {'words': '14排', 'probability': {'variance': 0.002354, 'average': 0.962852, 'min': 0.894295}}, {'words': '7排', 'probability': {'variance': 0.043623, 'average': 0.697632, 'min': 0.488772}}, {'words': '03排', 'probability': {'variance': 0.063906, 'average': 0.812009, 'min': 0.454596}}, {'words': '46', 'probability': {'variance': 0.0, 'average': 0.999721, 'min': 0.999466}}, {'words': 'MSTE SAELE SMOKE', 'probability': {'variance': 0.025206, 'average': 0.776894, 'min': 0.553879}}, {'words': 'NK DUSK CASABLANCE SOMETHNOWLD', 'probability': {'variance': 0.017596, 'average': 0.83199, 'min': 0.609927}}], 'language': -1}
    
    2: {'log_id': 7659937361977788002, 'words_result_num': 24, 'words_result': [{'words': '01#'}, {'words': '04#'}, {'words': '08#'}, {'words': '09#'}, {'words': '16#'}, {'words': 'SPANISH PO NDWN ROSE FLAMINGO TRUE CORAL SCARLET ROUC'}, {'words': '10#'}, {'words': '17#'}, {'words': '21#'}, {'words': '22#'}, {'words': '13#'}, {'words': 'CHERRY LUSH MOLET FATALE NOED CORNL. DOON PNX BLUSH NUDE'}, {'words': '45#'}, {'words': '47#'}, {'words': '49#'}, {'words': '15#'}, {'words': '23#'}, {'words': 'SHOWGIRLLLAC NYMPH MSBEHAVEDWLD ONCER BARE PEACH'}, {'words': '35#'}, {'words': '14#'}, {'words': '7#'}, {'words': '03#'}, {'words': '46#'}, {'words': 'SMELT MSTBRYSABLE SMOKE PINK DUSK CASABLANCESOMETHNOVLD'}]}
    
    3:{'log_id': 3261191746421964930, 'words_result_num': 26, 'words_result': [{'words': '01#'}, {'words': '04#'}, {'words': '08#'}, {'words': '09#'}, {'words': '16#'}, {'words': ' SPANISH PI DNOUN ROSE FLAMINGO TRUECORAL SCARLET ROUO'}, {'words': '10#'}, {'words': '17#'}, {'words': '21#'}, {'words': '22#'}, {'words': '13#'}, {'words': ' CHERRY LUSH VOLET FATALE NACED CORAL FORSDGEN BLUSHNUDE'}, {'words': '45#'}, {'words': '47#'}, {'words': '49#'}, {'words': '15#'}, {'words': '23#'}, {'words': ' SHOWGIRL ULAC NYMPH MSH8HVED WLD ONGER BARE PEACH'}, {'words': '35#'}, {'words': '14#'}, {'words': '7#'}, {'words': '03#'}, {'words': '46#'}, {'words': ' SWCETMYSTERY SABLE SMOKE'}, {'words': ' PINKDUSK'}, {'words': ' CASABLANCE SOMETNGWLD'}]}
    
    4:{'log_id': 4496045203345301378, 'words_result_num': 24, 'words_result': [{'words': '01#'}, {'words': '04#'}, {'words': '08#'}, {'words': '09#'}, {'words': '16#'}, {'words': ' SPAISH NDUN ROSE FLAMINGO TRUE CORAL SCARLET ROUCE'}, {'words': '10#'}, {'words': '17#'}, {'words': '21#'}, {'words': '22#'}, {'words': '13#'}, {'words': ' CHERRY LUSHVOLET FATALE NNCED CORAL FORSDOON BLUSH NUDE'}, {'words': '45#'}, {'words': '47#'}, {'words': '49#'}, {'words': '15#'}, {'words': '23#'}, {'words': ' SHOWGIRL UAC NYMPH MSBEHAV WLD ONNOER BARE PEACH'}, {'words': '35#'}, {'words': '14#'}, {'words': '7#'}, {'words': '03#'}, {'words': '46#'}, {'words': ' TMYSIYSABLE SMOKE PINK DUSK CASABUANCE SOMCTENGVOLD'}]}
    '''
    bd_ocr = BaiduOCR()
    ret = bd_ocr.basic_accurate(fp)
    print(ret)
    # for file in settings.TEST_IMAGE_FP:
    #     # print(file)
    #     colors = get_rgb_of_img_load(file)
    #     ano_color = get_rgb_of_img_getpixel(file)
    #     print(colors, ano_color)
