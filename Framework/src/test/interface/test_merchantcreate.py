# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-19 14:15:03
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-12 17:50:59

import requests,unittest,os,sys,time,json

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
# print (sys.path)
from src.utils.config import Config,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestReportCN import HTMLTestRunner
from src.utils.mail import Email
from src.utils.client import HTTPClient
from src.utils.extractor import JMESPathExtractor
from src.utils.generator import random_number
from src.utils.excel_write import writeExcel

class TestMerchantCreate(unittest.TestCase):
	"""商户创建接口"""
	API_URL = Config().get('OpenPlatform_API').get('Merchant').get('MerchantCreate')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_CreateMerchant01(self):
		"""简单验证商户创建接口容错"""
		datas = ExcelReader(self.excel,sheet='CreateMerchant').data
		for d in range(0,len(datas)):
			if datas[d]['is_execute'] == 'N':
				continue
			else:
				with self.subTest(data=datas[d]['CaseNo']+datas[d]['describe']):
					self.setUp()
					# logger.debug(datas[d])
					expect = datas[d]['expect_code']
					casename = str(datas[d]['describe'])
					caseNo = str(datas[d]['CaseNo'])
					#请求的参数剔除期望值列、是否执行列、描述列、用例编号列
					datas[d].pop('expect_code')
					datas[d].pop('is_execute')
					datas[d].pop('describe')
					datas[d].pop('CaseNo')
					if datas[d]['isOfficial'] == 'true':
						datas[d]['isOfficial'] = True
					elif datas[d]['isOfficial'] == 'false':
						datas[d]['isOfficial'] = False
					#转换为json格式
					params = json.dumps(datas[d])
					# logger.debug(type(params))
					headers={'Content-Type': "application/json"}
					res = self.client.send(data=params,headers=headers)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_CreateMerchant02(self):
		"""验证创建后数据返回"""
		datas = {"name": "中顺网络公司", "shortName": "ZS棋牌", "type": 1, "state": 1, "principal": "", "creditCode": "", "legalRepresentative": "", "mobile": "", "address": "", "contactName": "王小姐", "contactMobile": 19978953221, "email": "", "qq": 54321, "weChat": "", "businessLicense": "", "classicalChinese": "", "icp": "", "corporateIdentityCard": ""}
		headers={'Content-Type': "application/json"}

		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res = self.client.send(data=json.dumps(datas),headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + json.dumps(datas) + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(res.text),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertEqual(32, len(res_data), msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestMerchantCreate('test_CreateMerchant02'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
	# date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	# a = '2019-07-19'
	# b = '2019-07-19 17:23:58.016'
	# print (a in b)