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

class TestMall(unittest.TestCase):
	"""统一订单接口"""
	API_URL = Config().get('API_URL').get('Pay')
	excel = DATA_PATH + '\PayTest.xlsx'
	
	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')

	def tearDown(self):
		logger.info('测试结束')

	def test_productlist(self):
		"""钻石商城商品信息查询接口"""
		datas = ExcelReader(self.excel,sheet='ProductList').data
		for d in range(0,len(datas)):
			with self.subTest(data=datas[d]['describe']):
				self.setUp()
				# logger.debug(datas[d])
				expect = datas[d]['expectation']
				#请求的参数剔除期望值列、描述列
				datas[d].pop('expectation')
				datas[d].pop('describe')
				params = datas[d]
				res = self.client.send(data=params)
				# logger.debug(res.text)
				# result = JMESPathExtractor().extract(query='[0].itemName', body=res.text)
				self.assertEqual(expect, res.text)
				self.tearDown()

if __name__ == '__main__':
	report = REPORT_PATH + '\\report.html'
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='API测试框架', description='接口html报告')
		runner.run(TestMall('test_productlist'))

    