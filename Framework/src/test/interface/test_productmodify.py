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

class TestProductModify(unittest.TestCase):
	"""产品修改接口"""
	API_URL = Config().get('OpenPlatform_API').get('Product').get('Product')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='PATCH')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')

	def tearDown(self):
		logger.info('结束测试')

	def test_ProductModify01(self):
		"""简单验证修改产品接口容错"""
		datas = ExcelReader(self.excel,sheet='ModifyProduct').data
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
					if datas[d]['productId'] == '{pid1-0}':
						datas[d]['productId'] = OpenPlatformCommon.getpid(self.mid, category=1, platform=0)
					elif datas[d]['productId'] == '{pid1-1}':
						datas[d]['productId'] = OpenPlatformCommon.getpid(self.mid, category=1, platform=1)
					elif datas[d]['productId'] == '{pid2}':
						datas[d]['productId'] = OpenPlatformCommon.getpid(self.mid, category=2)
					elif datas[d]['productId'] == '{pid3}':
						datas[d]['productId'] = OpenPlatformCommon.getpid(self.mid, category=3)

					datas[d]['settings']= ast.literal_eval(datas[d]['settings'])
					# logger.debug(type(datas[d]['setting']))
					# logger.debug(datas[d]['setting'])
					#转换为json格式
					# json.dumps(datas[d]['settings'])
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

	def test_ProductModify02(self):
		"""验证修改产品接口-传入产品id不存在返回信息是否正确"""
		datas = {"productId": "39ef3eb319f97c3de783c27e5c47f908", "name": "AutoTest修改测试", "iconUrl": "", "department": "", "introduction": "", "state": 2, "settings": {"packageName": "AutoTest", "signature": "AutoTest"}}
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=json.dumps(datas),headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		error = JMESPathExtractor().extract(query='error', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + json.dumps(datas) + '\n返回结果:' + res.text
		self.assertEqual('false', str(result).lower(),msg=msg)
		self.assertEqual('修改产品失败，不存在编号为39ef3eb319f97c3de783c27e5c47f908的产品', str(error),msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)

	def test_ProductModify03(self):
		"""验证修改产品成功时返回信息是否正确"""
		pid = OpenPlatformCommon.getpid(self.mid, category=3)
		datas = {"productId": pid, "name": "AutoTest修改测试", "iconUrl": "", "department": "", "introduction": "", "state": 2, "settings": {"packageName": "AutoTest", "signature": "AutoTest", "smallProgramId": "AutoTestEdit",
    "smallPlatformType": 0}}
		headers={'Content-Type': "application/json"}
		res = self.client.send(data=json.dumps(datas),headers=headers)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + json.dumps(datas) + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知', str(message),msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)



if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestProductModify('test_ProductModify03'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)