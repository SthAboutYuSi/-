# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-29 17:30:59
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-17 11:21:52
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

class TestGetChannelTypeByCode(unittest.TestCase):
	"""产品渠道添加接口"""
	API_URL = Config().get('OpenPlatform_API').get('ProductChannel').get('GetChannelType')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_GetChannelTypeByCode01(self):
		"""简单验证获取渠道类型接口容错"""
		datas = ExcelReader(self.excel,sheet='GetChannelTypeByCode').data
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
					params = datas[d]					
					res = self.client.send(params=params)

					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_GetChannelTypeByCode02(self):
		"""验证获取渠道类型成功返回"""
		data = {"channelCode": 81026963}
		params = data
		res = self.client.send(params=params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		res_data = JMESPathExtractor().extract(query='data', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		res_id = JMESPathExtractor().extract(query='data.id', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertEqual(2, res_type, msg=msg)
		self.assertEqual('39ef7c14c2ae6187df4be0281eca0beb', res_id, msg=msg)
		self.tearDown()

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestGetChannelTypeByCode('test_GetChannelTypeByCode02'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)