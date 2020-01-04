# -*- coding: utf-8 -*-
"""
Convert number value to Thai read out

Adapted from
http://justmindthought.blogspot.com/2012/12/code-php.html
https://suksit.com/post/writing-bahttext-in-php/
"""
import math

__all__ = ["bahttext", "num_to_thaiword"]

def bahttext(number: float) -> str:
    """
    This function converts a number to Thai text and adds
    a suffix "บาท" (Baht).
    The precision will be fixed at two decimal places (0.00)
    to fits "สตางค์" (Satang) unit.
    This function works similar to `BAHTTEXT` function in MS Excel.

    :param float number: number to be converted into Thai Baht currency format
    :return: text representing the amount of money in the format
             of Thai currency
    :rtype: str
    :Example:
    ::

        from pythainlp.util import bahttext

        bahttext(1)
        # output: หนึ่งบาทถ้วน

        bahttext(21)
        # output: ยี่สิบเอ็ดบาทถ้วน

        bahttext(200)
        # output: สองร้อยบาทถ้วน
    """
    ret = ""

    if number is None:
        pass
    elif number == 0:
        ret = "ศูนย์บาทถ้วน"
    else:
        num_int, num_dec = "{:.2f}".format(number).split(".")
        num_int = int(num_int)
        if num_int < 0:
          ret = "ลบ"
          num_int *= -1

        num_dec = int(num_dec)

        baht = num_to_thaiword(num_int)
        if baht:
            ret = "".join([ret, baht, "บาท"])

        satang = num_to_thaiword(num_dec)
        if satang and satang != "ศูนย์":
            ret = "".join([ret, satang, "สตางค์"])
        else:
            ret = "".join([ret, "ถ้วน"])

    return ret


def num_to_thaiword(number: int) -> str:
    """
    This function convert number to Thai text

    :param int number: an integer number to be converted to Thai text
    :return: text representing the number in Thai
    :rtype: str

    :Example:
    ::

        from pythainlp.util import num_to_thaiword

        num_to_thaiword(1)
        # output: หนึ่ง

        num_to_thaiword(11)
        # output: สิบเอ็ด
    """
    values = ['', 'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า']
    places = ['', 'สิบ', 'ร้อย', 'พัน', 'หมื่น', 'แสน', 'ล้าน']
    exceptions = {'หนึ่งสิบ' : 'สิบ', 'สองสิบ' : 'ยี่สิบ', 'สิบหนึ่ง' : 'สิบเอ็ด'}

    output = ''
    if number == 0:
        output = "ศูนย์"
    
    number = str(number)
    for place,value in enumerate(list(number[::-1])):
        if (place % 6 == 0 and place > 0):
            output = places[6] + output

        if (value != '0'):
            output = values[int(value)] + places[place % 6] + output

    for search,replac in exceptions.items():
        output = output.replace(search,replac)
    
    return output
