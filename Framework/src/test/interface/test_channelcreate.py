# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-29 10:19:24
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-10 18:32:26

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

class TestChannelCreate(unittest.TestCase):
	"""渠道添加接口"""
	API_URL = Config().get('OpenPlatform_API').get('Channel').get('ChannelCreate')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ChannelCreate01(self):
		"""简单验证添加渠道接口容错"""
		datas = ExcelReader(self.excel,sheet='CreateChannel').data
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
					if datas[d]['id'] == '{mid}':
						datas[d]['id'] = self.mid

					#转换为json格式
					params = json.dumps(datas[d])
					
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

	def test_ChannelCreate02(self):
		"""验证创建成功后返回"""
		datas = {"name": "Autotest渠道创建成功", "type": 1, "developerPlatform": "Autotest自动化"}
		params = json.dumps(datas)	
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res_cid = JMESPathExtractor().extract(query='data', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertEqual(32, len(res_cid), msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestChannelCreate('test_ChannelCreate01'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
