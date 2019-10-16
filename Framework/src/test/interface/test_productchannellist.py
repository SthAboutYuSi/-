# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-29 17:30:59
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-17 10:31:09
import requests,unittest,os,sys,time,json,ast

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
# print (sys.path)
from src.utils.config import Config,DATA_PATH,REPORT_PATH
from src.utils.log import logger
from src.utils.file_reader import ExcelReader
from src.utils.HTMLTestReportCN import HTMLTestRunner
from src.utils.mail import Email
from src.utils.client import HTTPClient
from src.utils.extractor import JMESPathExtractor
from src.test.common.OpenPlatformCommon import OpenPlatformCommon

class TestProductChannelList(unittest.TestCase):
	"""产品渠道添加接口"""
	API_URL = Config().get('OpenPlatform_API').get('ProductChannel').get('ProductChannelList')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ProductChannelList01(self):
		"""简单验证添加产品渠道接口容错"""
		datas = ExcelReader(self.excel,sheet='ProductChannelList').data
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
					if datas[d]['ProductId'] == '{pid}':
						datas[d]['ProductId'] = OpenPlatformCommon.getpid(self.mid)
					# #转换为json格式
					# params = json.dumps(datas[d])
					params = datas[d]					
					# headers={'Content-Type': "application/json"}
					res = self.client.send(params=params)

					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_ProductChannelList02(self):
		"""验证产品渠道列表成功返回"""
		data = {"ProductId": "39ef7c0979b17b02ec4616b4384ff1c8"}
		params = data
		res = self.client.send(params=params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertEqual(4, len(res_data),msg=msg)
		self.tearDown()

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestProductChannelList('test_ProductChannelList02'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)