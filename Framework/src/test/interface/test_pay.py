import os,sys
import time
import unittest
import requests,unittest,os,time,json

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
# print (sys.path)
from src.utils.config import Config,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestRunner import HTMLTestRunner
from src.utils.mail import Email
from src.utils.client import HTTPClient
from src.utils.extractor import JMESPathExtractor
from src.utils.generator import random_number
from src.utils.excel_write import writeExcel

#取当前时间
now= time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
report = os.path.join(REPORT_PATH , now + 'report.html')
resultpath = os.path.join(REPORT_PATH , now + 'report.xlsx')

class TestPay(unittest.TestCase):
	"""统一订单接口"""
	API_URL = Config().get('API_URL').get('Pay')
	excel = DATA_PATH + '\PayAPI.xlsx'
	
	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')

	def tearDown(self):
		logger.info('测试结束')

	def test_pay(self):
		"""新平台"""
		datas = ExcelReader(self.excel,sheet='Pay').data
		resultdata= list()
		resultdata.insert(0,["用例名称","支付网关","网站商务识别号","返回结果"])
		for d in range(0,len(datas)):
			if datas[d]['is_execute'] == 'N':
				continue
			else:
				with self.subTest(data=datas[d]['describe']):
					self.setUp()
					# logger.debug(datas[d])

					expect = datas[d]['expect_code']
					casename = str(datas[d]['describe'])
					paygateway = str(datas[d]['gateway'])
					webid = str(datas[d]['identity'])
					# logger.debug('{0} {1} '.format(resultlist,paygateway))
					#随机生成订单号：13位时间戳+随机6个数字
					datas[d]['orderNO']=str(int(time.time()*1000)) + str(random_number())
					#请求的参数剔除期望值列、描述列、结果列，是否执行列
					datas[d].pop('expect_code')
					datas[d].pop('is_execute')
					datas[d].pop('describe')
					datas[d].pop('result')
					#转换为json格式
					params = json.dumps(datas[d])
					# logger.debug(type(params))
					headers={'Content-Type': "application/json"}
					res = self.client.send(data=params,headers=headers)
					resultlist =[casename,paygateway,webid,res.text] 
					resultdata.append(resultlist)						
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='code', body=res.text)
					self.assertEqual(expect, result)
					self.tearDown()
			
			# logger.debug(resultdata)			
			writeExcel(path=resultpath, data=resultdata)
					



if __name__ == '__main__':
	# report = REPORT_PATH + '\\report.html'
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='API测试框架', description='接口测试html报告')
		runner.run(TestPay('test_pay'))
	# data = [
	# 	["用例名称", "支付网关", "网站商务识别号", "返回结果"],
	# 	[1, "杨", 23, "2018-12-09","rewf0"],
	# 	[2, "张", 33, "2018-12-09", None, "很长很长的中文文字很长很长的中文文字很长很长的中文文字很长很长的中文文字"],
	# 	[3, "王", 42, "2018-12-10","长中文文字长中文文字长中文文字长中文文字"]
	# ]
	# a=[1,2,3,4]
	# data=list()
	# data.append(["用例名称1", "支付网关2", "网站商务识别号", "返回结果"])
	# data.insert(0,["222"])
	# print(data)
     