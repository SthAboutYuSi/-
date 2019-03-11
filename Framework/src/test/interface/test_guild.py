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

class TestGuild(unittest.TestCase):
	"""docstring for TestGuild"""
	API_URL = Config().get('API_URL').get('sss')
	excel = DATA_PATH + '\APITest.xlsx'
	
	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')

	def test_checkinfo(self):
		datas = ExcelReader(self.excel).data
		for d in range(0,len(datas)):
			logger.debug(datas[d])
			res = self.client.send(params=datas[d])
			logger.debug(res)
			print (res)

if __name__ == '__main__':
	report = REPORT_PATH + '\\report.html'
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='API测试框架', description='接口html报告')
		runner.run(TestGuild('test_checkinfo'))

    