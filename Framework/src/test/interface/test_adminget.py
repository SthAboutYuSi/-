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
from src.test.common.OpenPlatformCommon import OpenPlatformCommon

class TestAdminGet(unittest.TestCase):
	"""管理员详情接口"""
	API_URL = Config().get('OpenPlatform_API').get('Admin').get('AdminGet')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		self.mid = OpenPlatformCommon.getmid()
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_AdminGet01(self):
		"""简单验证获取管理员信息接口容错"""
		datas = ExcelReader(self.excel,sheet='GetAdmin').data		
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
					if datas[d]['id'] == '{aid}':
						datas[d]['id'] = OpenPlatformCommon.getaid(self.mid)[0]
					res = self.client.sendbyurl(datas[d]['id'])
					# resultlist =[caseNo,casename,params,expect,res.text] 
					# resultdata.qppend(resultlist)				
					# logger.debug(res.text)
					result = JMESPathExtractor().extract(query='success', body=res.text)
					message = JMESPathExtractor().extract(query='message', body=res.text)
					msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
					self.assertEqual(expect, str(result).lower(),msg=msg)
					self.assertNotIn('未知错误', str(message),msg=msg)
					self.tearDown()

	def test_AdminGet02(self):
		"""验证创建成功后获取管理员信息是否正确"""
		aid,account = OpenPlatformCommon.getaid(self.mid)

		date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		res = self.client.sendbyurl(aid)
		res_result = JMESPathExtractor().extract(query='success', body=res.text)
		res_aid = JMESPathExtractor().extract(query='data.id', body=res.text)
		res_mid = JMESPathExtractor().extract(query='data.mId', body=res.text)
		res_loginaccount = JMESPathExtractor().extract(query='data.loginAccount', body=res.text)
		res_mobile = JMESPathExtractor().extract(query='data.mobile', body=res.text)
		res_position = JMESPathExtractor().extract(query='data.position', body=res.text)
		res_realname = JMESPathExtractor().extract(query='data.realName', body=res.text)
		res_createtime = JMESPathExtractor().extract(query='data.createTime', body=res.text)
		res_state = JMESPathExtractor().extract(query='data.state', body=res.text)
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n请求数据:' + aid + '\n返回结果:' + res.text
		self.assertEqual('true', str(res_result).lower(),msg=msg)
		self.assertEqual(self.mid, res_mid, msg=msg)
		self.assertEqual(aid, res_aid, msg=msg)
		self.assertEqual(account, res_loginaccount, msg=msg)
		self.assertEqual('None', str(res_mobile), msg=msg)
		self.assertEqual('', str(res_position), msg=msg)
		self.assertEqual('', str(res_realname), msg=msg)
		self.assertEqual('1', str(res_state), msg=msg)
		self.assertEqual('1', str(res_type), msg=msg)
		self.assertIn(date, str(res_createtime), msg=msg)

	# def test_AdminGet03(self):
	# 	"""验证编辑成功后获取管理员信息是否正确"""
	# 	aid,account = OpenPlatformCommon.getaid(self.mid)
	# 	edit_datas ={"id": aid, "loginPassword": "aototestupDate123", "position": "自动化测试", "operator": 1, "realName": "自动化", "state": 2}
	# 	edit_headers={'Content-Type': "application/json"}
	# 	edit_url = Config().get('OpenPlatform_API').get('Admin').get('AdminEdit')
	# 	edit_client = HTTPClient(url=edit_url, method='POST')
	# 	edit_client.send(data=json.dumps(edit_datas),headers=edit_headers)
	# 	#查询管理员信息
	# 	res = self.client.sendbyurl(aid)

	# 	date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	# 	#获取返回的查询信息
	# 	res_result = JMESPathExtractor().extract(query='success', body=res.text)
	# 	res_aid = JMESPathExtractor().extract(query='data.id', body=res.text)
	# 	res_mid = JMESPathExtractor().extract(query='data.mId', body=res.text)
	# 	res_loginaccount = JMESPathExtractor().extract(query='data.loginAccount', body=res.text)
	# 	res_mobile = JMESPathExtractor().extract(query='data.mobile', body=res.text)
	# 	res_position = JMESPathExtractor().extract(query='data.position', body=res.text)
	# 	res_realname = JMESPathExtractor().extract(query='data.realName', body=res.text)
	# 	res_createtime = JMESPathExtractor().extract(query='data.createTime', body=res.text)
	# 	res_state = JMESPathExtractor().extract(query='data.state', body=res.text)
	# 	res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
	# 	msg = '\n请求地址：'+ res.url + '\n请求数据:' + aid + '\n返回结果:' + res.text
	# 	self.assertEqual('true', str(res_result).lower(),msg=msg)
	# 	self.assertEqual(self.mid, res_mid, msg=msg)
	# 	self.assertEqual(aid, res_aid, msg=msg)
	# 	self.assertEqual(account, res_loginaccount, msg=msg)
	# 	self.assertEqual('None', str(res_mobile), msg=msg)
	# 	self.assertEqual('自动化测试', str(res_position), msg=msg)
	# 	self.assertEqual('自动化', str(res_realname), msg=msg)
	# 	self.assertEqual('2', str(res_state), msg=msg)
	# 	self.assertEqual('3', str(res_type), msg=msg)
	# 	self.assertIn(date, str(res_createtime), msg=msg)

if __name__ == '__main__':
	report = os.path.join(REPORT_PATH , 'report.html')
	suite = unittest.TestSuite()
	suite.addTest(TestAdminGet('test_AdminGet02'))
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
		runner.run(suite)
