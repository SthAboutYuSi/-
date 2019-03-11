"""
文件读取。YamlReader读取yaml文件，ExcelReader读取excel。
"""

import yaml
import os,time
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
				for row in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
					#print(s.row_values(row))
					# for col in range(0, s.ncols):
					# 	#print (s.row_values(row)[col])
					# 	if s.row_values(row)[col] == 'nowtime' :
					# 		s.row_values(row)[col] = int(time.time())
					# 	print (s.row_values(row)[col])
					self._data.append(dict(zip(title, s.row_values(row))))
			else:
				for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
					self._data.append(s.row_values(col))
		return self._data

class readExcel():
	def get_xls(self, xlsPath, sheet_name):# xls_name填写用例的Excel名称 sheet_name该Excel的sheet名称
		cls = []
		file = open_workbook(xlsPath)# 打开用例Excel
		sheet = file.sheet_by_name(sheet_name)#获得打开Excel的sheet
        # 获取这个sheet内容行数
		nrows = sheet.nrows
		for i in range(nrows):#根据行数做循环
			if sheet.row_values(i)[0] != u'case_name':#如果这个Excel的这个sheet的第i行的第一列不等于case_name那么我们把这行的数据添加到cls[]
				cls.append(sheet.row_values(i))               
		return cls

if __name__ == '__main__':#我们执行该文件测试一下是否可以正确获取Excel中的值
	#print(readExcel().get_xls('E:\工作\Framework\data\APITest.xlsx', 'InfoCheck'))
	datas = ExcelReader('E:\工作\Framework\data\APITest.xlsx', 'sss').data
	print(datas)
	print (len(datas))
	# for i in len(datas):
	# 	print (datas[i])

# if __name__ == '__main__':
# 	#y = r'E:\工作\Framework\config\config.yaml'
# 	yaml = PathReader.get_Path()
# 	reader = YamlReader(y)
# 	print(reader.data)

# 	e = r'E:/工作/Framework/data/baidu.xlsx'
# 	reader = ExcelReader(e, title_line=True)
# 	print(reader.data)
		
		