# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-29 17:30:59
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-16 18:06:43
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

class TestProductChannelCreate(unittest.TestCase):
	"""产品渠道添加接口"""
	API_URL = Config().get('OpenPlatform_API').get('ProductChannel').get('ProductChannelCreate')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		self.mid = OpenPlatformCommon.getmid()
		self.cid = OpenPlatformCommon.getcid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ProductChannelCreate01(self):
		"""简单验证添加产品渠道接口容错"""
		datas = ExcelReader(self.excel,sheet='ProductChannel').data
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
					if datas[d]['productId'] == '{pid}':
						datas[d]['productId'] = OpenPlatformCommon.getpid(self.mid)
					if datas[d]['channelId'] == '{cid}':
						datas[d]['channelId'] = self.cid
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

	def test_ProductChannelCreate02(self):
		"""验证添加产品渠道成功后返回"""
		data = {"productId": "39ef52a391245e17ae89d8166ddfd666", "channelId": "39ef52a390e53c09739be5209d765d6b"}
		params = json.dumps(data)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestProductChannelCreate('test_ProductChannelCreate02'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)