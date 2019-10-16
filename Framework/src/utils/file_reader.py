# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-17 10:16:49
# @Last Modified by:   yusi
# @Last Modified time: 2019-07-19 11:06:00
"""
文件读取。YamlReader读取yaml文件，ExcelReader读取excel。
"""

import yaml
import os,time,json
from xlrd import open_workbook

class YamlReader:
	"""docstring for YamlReader"""
	def __init__(self, yamlf):
		if os.path.exists(yamlf):
			self.yamlf = yamlf
		else:
			raise FileNotFoundError('文件不存在！')
		self._data = None

	@property
	def data(self):
		#如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
		if not self._data:
			with open(self.yamlf,'rb') as f:
				self._data=list(yaml.safe_load_all(f))	#load后是个generator,用list组织成列表
		return self._data

class PathReader:
	
	def get_Path():
		"""读取项目某路径下某文件绝对路径"""
		path = os.path.split(os.path.realpath(__file__))[0]
		return path

	def get_WorkPath():
		"""读取当前执行文件的目录路径"""
		path = os.getcwd()
		return path


class SheetTypeError(Exception):
	"""docstring for SheetTypeError"""
	pass


class ExcelReader:
	"""
	读取excel文件中的内容，返回list。

	如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """
	def __init__(self, excel, sheet=0, title_line=True):
		if os.path.exists(excel):
			self.excel = excel
		else:
			raise FileNotFoundError('文件不存在！')
		self.sheet = sheet
		self.title_line = title_line
		self._data = list()

	@property
	def data(self):
		if not self._data:
			workbook = open_workbook(self.excel)
			if type(self.sheet) not in [int, str]:
				raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
			elif type(self.sheet) == int:
				s = workbook.sheet_by_index(self.sheet)
			else:
				s = workbook.sheet_by_name(self.sheet)

			if self.title_line:
				title = s.row_values(0)  # 首行为title
				#datatype = s.row_values(1)   #第2行为数据类型
				for row in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
					#print(s.row_values(row))
					value =s.row_values(row)
					for col in range(0, s.ncols):
						# print (value[col])
						# if s.row_values(row)[col] == 'nowtime' :
						# 	value[col] = int(time.time())
						# print (type(value[col]))
						if type(value[col]) == float:
							if value[col] % 1 == 0:
								value[col]=int(value[col])
							else:
								value[col]=float(value[col])
						elif type(value[col]) == str:
							value[col]=str(value[col])
						

					self._data.append(dict(zip(title, value)))
			else:
				for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
					self._data.append(s.row_values(col))
		return self._data

		
		