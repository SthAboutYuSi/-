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

class TestGuild(object):
	"""docstring for TestGuild"""
	API_URL = Config().get('API_URL').get('InfoCheck')
	excel = DATA_PATH + '\APITest.xlsx'

	def test_checkinfo(self):
		datas = ExcelReader(self.excel).data
		print (datas)

if __name__ == '__main__':
	unittest.main()

    