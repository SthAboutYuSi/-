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

class TestProductCreate(unittest.TestCase):
	"""产品添加接口"""
	API_URL = Config().get('OpenPlatform_API').get('Product').get('Product')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='POST')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ProductCreate01(self):
		"""简单验证添加产品接口容错"""
		datas = ExcelReader(self.excel,sheet='CreateProduct').data
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
					if datas[d]['merchantId'] == '{mid}':
						datas[d]['merchantId'] = self.mid

					datas[d]['setting']= ast.literal_eval(datas[d]['setting'])
					# logger.debug(type(datas[d]['setting']))
					# logger.debug(datas[d]['setting'])
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

	def test_ProductCreate02(self):
		"""验证添加产品成功后接口返回是否正确"""
		datas = {"merchantId": self.mid, "introduction": "Autotest", "name": "Autotesttrue", "department": "Web\u7814\u53d1\u90e8\u95e8", "ecology": 0, "iconUrl": "Autotest", "category": 1, "state": 1, "setting": {"platform": 0, "packageName": "Autotest", "signature": "Autotest", "bundleID": "Autotest.bundleID", "appId": "Autotest.appId", "h5Type": 0, "h5PlatformName": "AutotestH5", "h5Address": "Autotest.H5", "smallProgramId": "AutotestsmallProgramId", "smallPlatformType": 0}}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res_pid = JMESPathExtractor().extract(query='data', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertEqual(32, len(res_pid), msg=msg)

	def test_ProductCreate03(self):
		"""验证同一商户添加多个产品"""
		data1 = {"merchantId": self.mid, "introduction": "Autotest", "name": "Autotesttrue", "department": "Web\u7814\u53d1\u90e8\u95e8", "ecology": 0, "iconUrl": "Autotest", "category": 1, "state": 1, "setting": {"platform": 0, "packageName": "Autotest", "signature": "Autotest", "bundleID": "Autotest.bundleID", "appId": "Autotest.appId", "h5Type": 0, "h5PlatformName": "AutotestH5", "h5Address": "Autotest.H5", "smallProgramId": "AutotestsmallProgramId", "smallPlatformType": 0}}
		data2 = {"merchantId": self.mid, "introduction": "Autotest", "name": "Autotesttrue", "department": "Web\u7814\u53d1\u90e8\u95e8", "ecology": 0, "iconUrl": "Autotest", "category": 1, "state": 1, "setting": {"platform": 0, "packageName": "Autotest", "signature": "Autotest", "bundleID": "Autotest.bundleID", "appId": "Autotest.appId", "h5Type": 0, "h5PlatformName": "AutotestH5", "h5Address": "Autotest.H5", "smallProgramId": "AutotestsmallProgramId", "smallPlatformType": 0}}
		params1 = json.dumps(data1)
		params2 = json.dumps(data2)
		headers={'Content-Type': "application/json"}
		res1 = self.client.send(data=params1,headers=headers)
		res2 = self.client.send(data=params2,headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res2.text)
		message = JMESPathExtractor().extract(query='message', body=res2.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res2.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res1_pid = JMESPathExtractor().extract(query='data', body=res1.text)
		res2_pid = JMESPathExtractor().extract(query='data', body=res2.text)
		msg = '\n请求地址：'+ res2.url + '\n请求数据:' + params2 + '\n返回结果:' + res2.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertEqual(32, len(res2_pid), msg=msg)
		self.assertNotEqual(res1_pid, res2_pid, msg=msg)

	def test_ProductCreate04(self):
		"""验证异常：不存在的商户id添加产品"""
		datas = {"merchantId": "39ef4f45d8fc1abbf9a8657cb30afe1f", "introduction": "Autotest", "name": "Autotesttrue", "department": "Web\u7814\u53d1\u90e8\u95e8", "ecology": 0, "iconUrl": "Autotest", "category": 1, "state": 1, "setting": {"platform": 0, "packageName": "Autotest", "signature": "Autotest", "bundleID": "Autotest.bundleID", "appId": "Autotest.appId", "h5Type": 0, "h5PlatformName": "AutotestH5", "h5Address": "Autotest.H5", "smallProgramId": "AutotestsmallProgramId", "smallPlatformType": 0}}
		params = json.dumps(datas)
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=params,headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res_pid = JMESPathExtractor().extract(query='data', body=res.text)
		res_error = JMESPathExtractor().extract(query='error', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + params + '\n返回结果:' + res.text
		self.assertEqual('false', str(result).lower(),msg=msg)
		self.assertNotIn('未知错误', str(message),msg=msg)
		self.assertIn(date, str(responseTime),msg=msg)
		self.assertIsNone(res_pid, msg=msg)
		self.assertEqual('创建产品失败，不存在id为39ef4f45d8fc1abbf9a8657cb30afe1f的商户', res_error, msg=msg)



if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestProductCreate('test_ProductCreate01'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
	# s = '{"ssssssss":1, "bbbb":2}'
	# print(type(s))
	# s= ast.literal_eval(s)
	# print(type(s))