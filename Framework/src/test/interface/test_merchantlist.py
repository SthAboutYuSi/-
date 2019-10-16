# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-19 14:55:27
# @Last Modified by:   yusi
# @Last Modified time: 2019-09-16 14:27:05
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


class TestMerchantList(unittest.TestCase):
	"""商户列表接口"""
	API_URL = Config().get('OpenPlatform_API').get('Merchant').get('MerchantList')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_GetMerchantList01(self):
		"""简单验证商户列表接口容错"""
		datas = ExcelReader(self.excel,sheet='MerchantList').data
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
					# params = json.dumps(datas[d])
					params = datas[d]
					# logger.debug(type(params))
					# headers={'Content-Type': "application/json"}
					res = self.client.send(params=params)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_GetMerchantList02(self):
		"""验证商户编号查询"""
		mid = OpenPlatformCommon.getmid()
		mcode,mname,mshortname,mtype,mtypename,mstate,mstatename = OpenPlatformCommon.getmcode(mid)
		params = {'keyword': mcode, 'pageIndex': 1, 'pageSize': 10}
		res = self.client.send(params=params)
		res_result = JMESPathExtractor().extract(query='success', body=res.text)
		res_datalength = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		res_mid = JMESPathExtractor().extract(query='data.data[0].id', body=res.text)
		res_mcode = JMESPathExtractor().extract(query='data.data[0].code', body=res.text)
		res_mname = JMESPathExtractor().extract(query='data.data[0].name', body=res.text)
		res_mshortname= JMESPathExtractor().extract(query='data.data[0].shortName', body=res.text)
		res_mtype = JMESPathExtractor().extract(query='data.data[0].type', body=res.text)
		#返回的商户类型名称
		res_mtypename = JMESPathExtractor().extract(query='data.data[0].typeName', body=res.text)
		#返回的商户状态值
		res_mstate = JMESPathExtractor().extract(query='data.data[0].state', body=res.text)
		#返回的商户状态
		res_mstatename = JMESPathExtractor().extract(query='data.data[0].stateName', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(res_result).lower(),msg=msg)
		self.assertEqual(1, res_datalength,msg=msg)
		self.assertEqual(mid, str(res_mid),msg=msg)
		self.assertEqual(mname, str(res_mname),msg=msg)
		self.assertEqual(mshortname, str(res_mshortname),msg=msg)	
		self.assertEqual(mtype, res_mtype,msg=msg)
		self.assertEqual(mtypename, str(res_mtypename),msg=msg)
		self.assertEqual(mstate, res_mstate,msg=msg)
		self.assertEqual(mstatename, str(res_mstatename),msg=msg)

	def test_GetMerchantList03(self):
		"""验证商户名称查询"""
		mid = OpenPlatformCommon.getmid()
		mcode,mname,mshortname,mtype,mtypename,mstate,mstatename = OpenPlatformCommon.getmcode(mid)
		params = {'keyword': mname, 'pageIndex': 1, 'pageSize': 10}
		res = self.client.send(params=params)
		res_result = JMESPathExtractor().extract(query='success', body=res.text)
		res_datalength = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		res_data = JMESPathExtractor().extract(query='data.data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(res_result).lower(),msg=msg)
		self.assertLessEqual(1, res_datalength,msg=msg)
		self.assertIn(mname, str(res_data),msg=msg)
		# self.assertIn(mcode, str(res_data),msg=res.text)

	def test_GetMerchantList04(self):
		"""验证商户简称查询"""
		mid = OpenPlatformCommon.getmid()
		mcode,mname,mshortname,mtype,mtypename,mstate,mstatename = OpenPlatformCommon.getmcode(mid)
		params = {'keyword': mshortname, 'pageIndex': 1, 'pageSize': 10000}
		res = self.client.send(params=params)
		res_result = JMESPathExtractor().extract(query='success', body=res.text)
		res_datalength = JMESPathExtractor().extract(query='data.recordsTotal', body=res.text)
		res_data = JMESPathExtractor().extract(query='data.data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(res_result).lower(),msg=msg)
		self.assertTrue(1 <= res_datalength,msg=msg)
		self.assertIn(mshortname, str(res_data),msg=msg)
		self.assertIn(mcode, str(res_data),msg=msg)