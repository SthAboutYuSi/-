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

def test_checkinfo():
	pass
	
	
	# for d in range(0,len(datas)):
	# 	print (datas[d])
	# 	res = client.send(params=datas[d])
	# 	print(res)
		#self.assertEqual(0, res.code)
	

if __name__ == '__main__':
	API_URL = Config().get('API_URL').get('sss')
	excel = DATA_PATH + '\APITest.xlsx'
	datas = ExcelReader(excel=excel,sheet='sss').data
	for d in range(0,len(datas)):
		print (datas[d])
		res = client.send(params=datas[d])
		print(res)