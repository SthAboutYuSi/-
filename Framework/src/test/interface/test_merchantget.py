# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-19 14:50:16
# @Last Modified by:   yusi
# @Last Modified time: 2019-08-06 18:19:38
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


class TestMerchantGet(unittest.TestCase):
	"""商户查询接口"""
	API_URL = Config().get('OpenPlatform_API').get('Merchant').get('MerchantGet')
	excel = DATA_PATH + '/OpenPlatform_Merchant.xlsx'

	def setUp(self):
		self.client = HTTPClient(url=self.API_URL, method='GET')
		logger.info('开始测试')


	def tearDown(self):
		logger.info('结束测试')

	def test_GetMerchant01(self):
		"""简单验证商户查询接口容错"""
		datas = ExcelReader(self.excel,sheet='GetMerchant').data
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
						datas[d]['id'] = OpenPlatformCommon.getmid()
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
					self.assertNotIn('未知', str(message),msg=msg)
					self.tearDown()

	def test_GetMerchant02(self):
		"""验证创建成功后查询接口返回信息是否正确"""
		mid = OpenPlatformCommon.getmid()
		params = {"id": mid}
		res = self.client.send(params=params)
		#返回的success值
		result = JMESPathExtractor().extract(query='success', body=res.text)
		#返回的商户id
		res_id = JMESPathExtractor().extract(query='data.id', body=res.text)
		#返回的商户名称
		res_name = JMESPathExtractor().extract(query='data.name', body=res.text)
		#返回的商户简称
		res_shortname = JMESPathExtractor().extract(query='data.shortName', body=res.text)
		#返回的商户类型
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		#返回的商户类型名称
		res_typename = JMESPathExtractor().extract(query='data.typeName', body=res.text)
		#返回的商户状态值
		res_state = JMESPathExtractor().extract(query='data.state', body=res.text)
		#返回的商户状态
		res_statename = JMESPathExtractor().extract(query='data.stateName', body=res.text)
		#返回的商户主体
		res_principal = JMESPathExtractor().extract(query='data.principal', body=res.text)
		#返回的社会统一信用码
		res_creditcode = JMESPathExtractor().extract(query='data.creditCode', body=res.text)
		#返回的法人信息
		res_legalrepresentative = JMESPathExtractor().extract(query='data.legalRepresentative', body=res.text)
		#返回的联系电话
		res_mobile = JMESPathExtractor().extract(query='data.mobile', body=res.text)
		#返回的地址
		res_address = JMESPathExtractor().extract(query='data.address', body=res.text)
		#返回的联系人名称
		res_contactname = JMESPathExtractor().extract(query='data.contactName', body=res.text)
		#返回的联系人手机
		res_contactmobile = JMESPathExtractor().extract(query='data.contactMobile', body=res.text)
		#返回的联系人邮箱地址
		res_email = JMESPathExtractor().extract(query='data.email', body=res.text)
		#返回的联系人QQ号码
		res_qq = JMESPathExtractor().extract(query='data.qq', body=res.text)
		#返回的联系人微信号
		res_wechat = JMESPathExtractor().extract(query='data.weChat', body=res.text)
		#返回的营业执照
		res_businesslicense = JMESPathExtractor().extract(query='data.businessLicense', body=res.text)
		#返回的文网文
		res_classicalchinese = JMESPathExtractor().extract(query='data.classicalChinese', body=res.text)
		#返回的ICP
		res_icp = JMESPathExtractor().extract(query='data.icp', body=res.text)
		#返回的法人身份证
		res_corporateidentitycard = JMESPathExtractor().extract(query='data.corporateIdentityCard', body=res.text)
		
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text

		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertEqual(mid, str(res_id), msg=msg)
		self.assertEqual('中顺网络公司', str(res_name), msg=msg)
		self.assertEqual('ZS棋牌', str(res_shortname), msg=msg)
		self.assertEqual('1', str(res_type), msg=msg)
		self.assertEqual('自研', str(res_typename), msg=msg)
		self.assertEqual('1', str(res_state), msg=msg)
		self.assertEqual('正常', str(res_statename), msg=msg)
		self.assertEqual('中顺棋牌', str(res_principal), msg=msg)
		self.assertEqual('91440106589536704F', str(res_creditcode), msg=msg)
		self.assertEqual('李石头', str(res_legalrepresentative), msg=msg)
		self.assertEqual('39956888', str(res_mobile), msg=msg)
		self.assertEqual('广东省广州市天河区天河软件园建中路50号多玩游戏大厦4楼', str(res_address), msg=msg)
		self.assertEqual('王小姐', str(res_contactname), msg=msg)
		self.assertEqual('19978953221', str(res_contactmobile), msg=msg)
		self.assertEqual('ZS@qq.com', str(res_email), msg=msg)
		self.assertEqual('54321', str(res_qq), msg=msg)
		self.assertEqual('qkagame', str(res_wechat), msg=msg)
		self.assertIn('20190722/953ba822fb8643b282e6102712d96c24.jpg', str(res_businesslicense), msg=msg)
		self.assertIn('20190722/c5e60fd2961b97aca2ea3ec735892a40.jpg', str(res_classicalchinese), msg=msg)
		self.assertIn('20190722/056fa26e44814b1ea36b288df9523f2f.jpeg', str(res_icp), msg=msg)
		self.assertIn('20190722/9fc2f9a61ae8486084f69ea6393f637d.jpeg', str(res_corporateidentitycard), msg=msg)

	def test_GetMerchant03(self):
		"""验证编辑成功后查询接口返回信息是否正确"""
		mid = OpenPlatformCommon.getmid()
		#编辑商户信息
		edit_datas = {"id": mid, "name": "编辑网络公司", "shortName": "ZS", "state": 2, "principal": "", "creditCode": "", "legalRepresentative": "", "mobile": "19978953221", "address": "", "contactName": "张小金", "contactMobile": 13778953221, "email": "ZS@qq.com", "qq":123456, "weChat": "weixin", "businessLicense": "20190723/953ba822fb8643b282e6102712d00024.jpg", "classicalChinese": "20190723/c5e60fd2961b97aca2ea3ec735891111.jpg", "icp": "20190723/056fa26e44814b1ea36b288df9522222.jpeg", "corporateIdentityCard": "20190723/9fc2f9a61ae8486084f69ea6393f3333.jpeg"}
		edit_headers={'Content-Type': "application/json"}
		edit_url = Config().get('OpenPlatform_API').get('Merchant').get('MerchantEdit')
		edit_client = HTTPClient(url=edit_url, method='POST')
		edit_client.send(data=json.dumps(edit_datas),headers=edit_headers)
		#查询商户信息
		params = {"id": mid}
		res = self.client.send(params=params)
		#返回的success值
		result = JMESPathExtractor().extract(query='success', body=res.text)
		#返回的商户id
		res_id = JMESPathExtractor().extract(query='data.id', body=res.text)
		#返回的商户名称
		res_name = JMESPathExtractor().extract(query='data.name', body=res.text)
		#返回的商户简称
		res_shortname = JMESPathExtractor().extract(query='data.shortName', body=res.text)
		#返回的商户类型
		res_type = JMESPathExtractor().extract(query='data.type', body=res.text)
		#返回的商户类型名称
		res_typename = JMESPathExtractor().extract(query='data.typeName', body=res.text)
		#返回的商户状态值
		res_state = JMESPathExtractor().extract(query='data.state', body=res.text)
		#返回的商户状态
		res_statename = JMESPathExtractor().extract(query='data.stateName', body=res.text)
		#返回的商户主体
		res_principal = JMESPathExtractor().extract(query='data.principal', body=res.text)
		#返回的社会统一信用码
		res_creditcode = JMESPathExtractor().extract(query='data.creditCode', body=res.text)
		#返回的法人信息
		res_legalrepresentative = JMESPathExtractor().extract(query='data.legalRepresentative', body=res.text)
		#返回的联系电话
		res_mobile = JMESPathExtractor().extract(query='data.mobile', body=res.text)
		#返回的地址
		res_address = JMESPathExtractor().extract(query='data.address', body=res.text)
		#返回的联系人名称
		res_contactname = JMESPathExtractor().extract(query='data.contactName', body=res.text)
		#返回的联系人手机
		res_contactmobile = JMESPathExtractor().extract(query='data.contactMobile', body=res.text)
		#返回的联系人邮箱地址
		res_email = JMESPathExtractor().extract(query='data.email', body=res.text)
		#返回的联系人QQ号码
		res_qq = JMESPathExtractor().extract(query='data.qq', body=res.text)
		#返回的联系人微信号
		res_wechat = JMESPathExtractor().extract(query='data.weChat', body=res.text)
		#返回的营业执照
		res_businesslicense = JMESPathExtractor().extract(query='data.businessLicense', body=res.text)
		#返回的文网文
		res_classicalchinese = JMESPathExtractor().extract(query='data.classicalChinese', body=res.text)
		#返回的ICP
		res_icp = JMESPathExtractor().extract(query='data.icp', body=res.text)
		#返回的法人身份证
		res_corporateidentitycard = JMESPathExtractor().extract(query='data.corporateIdentityCard', body=res.text)
		msg = '\n请求地址：'+ res.url + '\n返回结果:' + res.text
		self.assertEqual('true', str(result).lower(), msg=msg)
		self.assertEqual(mid, str(res_id), msg=msg)
		self.assertEqual('编辑网络公司', str(res_name), msg=msg)
		self.assertEqual('ZS', str(res_shortname), msg=msg)
		self.assertEqual('1', str(res_type), msg=msg)
		self.assertEqual('自研', str(res_typename), msg=msg)
		self.assertEqual('2', str(res_state), msg=msg)
		self.assertEqual('禁用', str(res_statename), msg=msg)
		self.assertEqual('', str(res_principal), msg=msg)
		self.assertEqual('', str(res_creditcode), msg=msg)
		self.assertEqual('', str(res_legalrepresentative), msg=msg)
		self.assertEqual('19978953221', str(res_mobile), msg=msg)
		self.assertEqual('', str(res_address), msg=msg)
		self.assertEqual('张小金', str(res_contactname), msg=msg)
		self.assertEqual('13778953221', str(res_contactmobile), msg=msg)
		self.assertEqual('ZS@qq.com', str(res_email), msg=msg)
		self.assertEqual('123456', str(res_qq), msg=msg)
		self.assertEqual('weixin', str(res_wechat), msg=msg)
		self.assertIn('20190723/953ba822fb8643b282e6102712d00024.jpg', str(res_businesslicense), msg=msg)
		self.assertIn('20190723/c5e60fd2961b97aca2ea3ec735891111.jpg', str(res_classicalchinese), msg=msg)
		self.assertIn('20190723/056fa26e44814b1ea36b288df9522222.jpeg', str(res_icp), msg=msg)
		self.assertIn('20190723/9fc2f9a61ae8486084f69ea6393f3333.jpeg', str(res_corporateidentitycard), msg=msg)


