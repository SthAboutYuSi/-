# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-17 10:16:49
# @Last Modified by:   yusi
# @Last Modified time: 2019-07-17 11:57:50
"""

读取配置。这里配置文件用的yaml，也可以用其它XML，INI等，需在file_reader中添加相应的Reader进行处理。

"""

import os
from src.utils.file_reader import YamlReader



BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yaml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')

class Config:
	"""读取配置文件"""
	def __init__(self, config=CONFIG_FILE):
		self.config = YamlReader(config).data

	def get(self,element,index=0):
		"""
		yaml是可以通过‘---’分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有很多节，可以传入index来获取。
		这样我们其实可以把框架相关的配置放在默认节，其它的关于项目的配置放在其它节中。可以在框架中实现多个项目的测试。

		"""
		return self.config[index].get(element)
