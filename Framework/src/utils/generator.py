# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-17 10:16:49
# @Last Modified by:   yusi
# @Last Modified time: 2019-08-16 16:20:47
"""一些生成器方法，生成随机数，手机号，以及连续数字等"""
import random
from faker import Factory

fake = Factory().create('zh_CN')


def random_phone_number():
    """随机手机号"""
    return fake.phone_number()


def random_name():
    """随机姓名"""
    return fake.name()


def random_address():
    """随机地址"""
    return fake.address()


def random_email():
    """随机email"""
    return fake.email()


def random_ipv4():
    """随机IPV4地址"""
    return fake.ipv4()

def random_barcode(length=8):
    """随机8位或者13位条码"""
    return fake.ean(length)

def random_number(digits=6):
    """随机数字，digits为数字位数"""
    return fake.random_number(digits)

def  random_password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True):
    return fake.password(length, special_chars, digits, upper_case, lower_case)

def random_str(min_chars=0, max_chars=8):
    """长度在最大值与最小值之间的随机字符串"""
    return fake.pystr(min_chars=min_chars, max_chars=max_chars)


def factory_generate_ids(starting_id=1, increment=1):
    """ 返回一个生成器函数，调用这个函数产生生成器，从starting_id开始，步长为increment。 """
    def generate_started_ids():
        val = starting_id
        local_increment = increment
        while True:
            yield val
            val += local_increment
    return generate_started_ids


def factory_choice_generator(values):
    """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
    def choice_generator():
        my_list = list(values)
        # rand = random.Random()
        while True:
            yield random.choice(my_list)
    return choice_generator

if __name__ == '__main__':
    # print(random_phone_number())
    # print(random_name())
    print(random_password(length=50, special_chars=False, digits=True, upper_case=True, lower_case=True))
    # print(random_address())
    # print(random_email())
    # print(random_ipv4())
     # print(random_address())
    print(random_str(min_chars=6, max_chars=8)+str(random_number()))
    # id_gen = factory_generate_ids(starting_id=1001, increment=1)()
    # for i in range(5):
    #     print(next(id_gen))

    # choices = ['John', 'Sam', 'Lily', 'Rose']
    # choice_gen = factory_choice_generator(choices)()
    # for i in range(5):
    #     print(next(choice_gen))
