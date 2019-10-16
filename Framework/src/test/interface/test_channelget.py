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
from src.test.common.OpenPlatformCommon import OpenPlatformCommon


class TestChannelGet(unittest.TestCase):
	"""渠道查询接口"""
	API_URL = Config().get('OpenPlatform_API').get('Channel').get('ChannelGet')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		self.cid = OpenPlatformCommon.getcid()
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_GetChannel01(self):
		"""简单验证渠道查询接口容错"""
		datas = ExcelReader(self.excel,sheet='ChannelDetail').data
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
					if datas[d]['id'] == '{cid}':
						datas[d]['id'] = self.cid
					#转换为json格式
					# params = json.dumps(datas[d])
					params = datas[d]['id']
					# logger.debug(type(params))
					# headers={'Content-Type': "application/json"}
					res = self.client.sendbyurl(params)
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知', str(message),msg=msg)
					self.tearDown()

	def test_GetChannel02(self):
		"""验证渠道创建成功后渠道查询接口返回"""
		params = self.cid
		res = self.client.sendbyurl(params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		error = JMESPathExtractor().extract(query='error', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_cid = JMESPathExtractor().extract(query='data.id', body=res.text)
		res_code = JMESPathExtractor().extract(query='data.code', body=res.text)
		res_name = JMESPathExtractor().extract(query='data.name', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		res_devplatform = JMESPathExtractor().extract(query='data.developerPlatform', body=res.text)
		res_createtime = JMESPathExtractor().extract(query='data.createTime', body=res.text)
		res_loginmodeid = JMESPathExtractor().extract(query='data.loginModeId', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知', str(message),msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertIsNone(error, msg=msg)
		self.assertEqual(self.cid, res_cid, msg=msg)
		self.assertEqual('Autotest渠道测试', res_name, msg=msg)
		self.assertEqual(1, res_type, msg=msg)
		self.assertEqual('Autotest开发者平台', res_devplatform, msg=msg)
		self.assertEqual('', res_loginmodeid, msg=msg)

	def test_GetChannel03(self):
		"""验证渠道编辑成功后渠道查询接口返回"""
		edit_datas = {"id": self.cid, "name": "ModifyAotuTest", "type": 4, "developerPlatform": "ModifyAotuTestChannel888"}
		edit_headers={'Content-Type': "application/json"}
		edit_url = Config().get('OpenPlatform_API').get('Channel').get('ChannelModify')
		edit_client = HTTPClient(url=edit_url, method='POST')
		edit_client.send(data=json.dumps(edit_datas),headers=edit_headers)
		params = self.cid
		res = self.client.sendbyurl(params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		error = JMESPathExtractor().extract(query='error', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_cid = JMESPathExtractor().extract(query='data.id', body=res.text)
		res_code = JMESPathExtractor().extract(query='data.code', body=res.text)
		res_name = JMESPathExtractor().extract(query='data.name', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		res_devplatform = JMESPathExtractor().extract(query='data.developerPlatform', body=res.text)
		res_createtime = JMESPathExtractor().extract(query='data.createTime', body=res.text)
		res_loginmodeid = JMESPathExtractor().extract(query='data.loginModeId', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(),msg=msg)
		self.assertNotIn('未知', str(message),msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertIsNone(error, msg=msg)
		self.assertEqual(self.cid, res_cid, msg=msg)
		self.assertEqual('ModifyAotuTest', res_name, msg=msg)
		self.assertEqual(4, res_type, msg=msg)
		self.assertEqual('ModifyAotuTestChannel888', res_devplatform, msg=msg)
		self.assertEqual('', res_loginmodeid, msg=msg)

	def test_GetChannel04(self):
		"""验证异常：渠道id不存在时查询接口返回"""
		params = '39ef53f9bd625593a1b7bea82dfebf9c'
		res = self.client.sendbyurl(params)
		result = JMESPathExtractor().extract(query='success', body=res.text)
		message = JMESPathExtractor().extract(query='message', body=res.text)
		error = JMESPathExtractor().extract(query='error', body=res.text)
		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		responseTime = JMESPathExtractor().extract(query='responseTime', body=res.text)
		res_cid = JMESPathExtractor().extract(query='data.id', body=res.text)
		res_code = JMESPathExtractor().extract(query='data.code', body=res.text)
		res_name = JMESPathExtractor().extract(query='data.name', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		res_devplatform = JMESPathExtractor().extract(query='data.developerPlatform', body=res.text)
		res_createtime = JMESPathExtractor().extract(query='data.createTime', body=res.text)
		res_loginmodeid = JMESPathExtractor().extract(query='data.loginModeId', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('false', str(result).lower(),msg=msg)
		self.assertNotIn('未知', str(message),msg=msg)
		self.assertIn(date, str(responseTime), msg=msg)
		self.assertIsNone(res_cid, msg=msg)
		self.assertEqual('渠道不存在或已删除！', error, msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestChannelGet('test_GetChannel04'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
