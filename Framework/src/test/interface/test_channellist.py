# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-29 16:24:41
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-12 17:47:39
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
from src.test.common.OpenPlatformCommon import OpenPlatformCommon


class TestChannelList(unittest.TestCase):
	"""渠道列表接口"""
	API_URL = Config().get('OpenPlatform_API').get('Channel').get('ChannelList')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_ChannelList01(self):
		"""简单验证渠道列表接口容错"""
		datas = ExcelReader(self.excel,sheet='ChannelList').data
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
					#转换为json格式
					params = json.dumps(datas[d])
					# logger.debug(type(params))
					headers={'Content-Type': "application/json"}
					res = self.client.send(data=params, headers=headers)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(), msg=msg)
					self.assertNotIn('未知错误', str(message), msg=msg)
					self.tearDown()

	def test_ChannelList02(self):
		"""验证渠道名称查询"""	
		datas = {"keyword": "官方", "pageIndex": 1, "pageSize": 10}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params, headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_id = JMESPathExtractor().extract(query='data.data[0].id', body=res.text)
		res_code = JMESPathExtractor().extract(query='data.data[0].code', body=res.text)
		res_name = JMESPathExtractor().extract(query='data.data[0].name', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.data[0].type', body=res.text)
		res_developerPlatform = JMESPathExtractor().extract(query='data.data[0].developerPlatform', body=res.text)
		res_createTime = JMESPathExtractor().extract(query='data.data[0].createTime', body=res.text)
		res_loginModeId = JMESPathExtractor().extract(query='data.data[0].loginModeId', body=res.text)
		res_loginMethod = JMESPathExtractor().extract(query='data.data[0].loginMethod', body=res.text)
		res_paymentTemplateId = JMESPathExtractor().extract(query='data.data[0].paymentTemplateId', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual('39ef7c11112bcb0abb399595e966846e', res_id, msg=msg)
		self.assertEqual('6962', res_code, msg=msg)
		self.assertEqual('测试基础数据_官方渠道', res_name, msg=msg)
		self.assertEqual(1, res_type, msg=msg)
		self.assertEqual('test', res_developerPlatform, msg=msg)
		self.assertEqual('2019-08-08T16:12:13', res_createTime, msg=msg)
		self.assertIsNone(res_loginMethod, msg=msg)
		self.assertIsNone(res_loginModeId, msg=msg)
		self.assertIsNone(res_paymentTemplateId, msg=msg)

	def test_ChannelList03(self):
		"""验证渠道编码查询"""	
		datas = {"keyword": "6963", "pageIndex": 1, "pageSize": 10}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params, headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_id = JMESPathExtractor().extract(query='data.data[0].id', body=res.text)
		res_code = JMESPathExtractor().extract(query='data.data[0].code', body=res.text)
		res_name = JMESPathExtractor().extract(query='data.data[0].name', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.data[0].type', body=res.text)
		res_developerPlatform = JMESPathExtractor().extract(query='data.data[0].developerPlatform', body=res.text)
		res_createTime = JMESPathExtractor().extract(query='data.data[0].createTime', body=res.text)
		res_loginModeId = JMESPathExtractor().extract(query='data.data[0].loginModeId', body=res.text)
		res_loginMethod = JMESPathExtractor().extract(query='data.data[0].loginMethod', body=res.text)
		res_paymentTemplateId = JMESPathExtractor().extract(query='data.data[0].paymentTemplateId', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual('39ef7c14c2ae6187df4be0281eca0beb', res_id, msg=msg)
		self.assertEqual('6963', res_code, msg=msg)
		self.assertEqual('测试基础数据_联运渠道', res_name, msg=msg)
		self.assertEqual(2, res_type, msg=msg)
		self.assertEqual('test', res_developerPlatform, msg=msg)
		self.assertEqual('2019-08-08T16:12:13', res_createTime, msg=msg)
		self.assertEqual('测试基础数据_登录方式_联运SDK', res_loginMethod, msg=msg)
		self.assertEqual('39ef7c13f0e8827efe3fae844d518713', res_loginModeId, msg=msg)
		# self.assertEqual('7d518dfd-62c3-4636-8909-15be17d964be',res_paymentTemplateId, msg=msg)
		self.assertIsNone(res_paymentTemplateId, msg=msg)

	def test_ChannelList04(self):
		"""验证渠道id查询"""	
		datas = {"keyword": "39ef7c14c2ae6187df4be0281eca0beb", "pageIndex": 1, "pageSize": 10}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params, headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_id = JMESPathExtractor().extract(query='data.data[0].id', body=res.text)
		res_code = JMESPathExtractor().extract(query='data.data[0].code', body=res.text)
		res_name = JMESPathExtractor().extract(query='data.data[0].name', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.data[0].type', body=res.text)
		res_developerPlatform = JMESPathExtractor().extract(query='data.data[0].developerPlatform', body=res.text)
		res_createTime = JMESPathExtractor().extract(query='data.data[0].createTime', body=res.text)
		res_loginModeId = JMESPathExtractor().extract(query='data.data[0].loginModeId', body=res.text)
		res_loginMethod = JMESPathExtractor().extract(query='data.data[0].loginMethod', body=res.text)
		res_paymentTemplateId = JMESPathExtractor().extract(query='data.data[0].paymentTemplateId', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertIsNone(res_error, msg=msg)
		self.assertEqual('39ef7c14c2ae6187df4be0281eca0beb', res_id, msg=msg)
		self.assertEqual('6963', res_code, msg=msg)
		self.assertEqual('测试基础数据_联运渠道', res_name, msg=msg)
		self.assertEqual(2, res_type, msg=msg)
		self.assertEqual('test', res_developerPlatform, msg=msg)
		self.assertEqual('2019-08-08T16:12:13', res_createTime, msg=msg)
		self.assertEqual('测试基础数据_登录方式_联运SDK', res_loginMethod, msg=msg)
		self.assertEqual('39ef7c13f0e8827efe3fae844d518713', res_loginModeId, msg=msg)
		# self.assertEqual('7d518dfd-62c3-4636-8909-15be17d964be',res_paymentTemplateId, msg=msg)
		self.assertIsNone(res_paymentTemplateId, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestChannelList('test_ChannelList04'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)