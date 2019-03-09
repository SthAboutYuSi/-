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

def test_checkinfo(self):
	API_URL = Config().get('API_URL').get('InfoCheck')
	excel = DATA_PATH + '\APITest.xlsx'
	
	datas = ExcelReader(self.excel).data
	return datas
	

if __name__ == '__main__':
	print('测试路径是否OK,路径为：', test_checkinfo())