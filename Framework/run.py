# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-17 09:22:13
# @Last Modified by:   yusi
# @Last Modified time: 2019-10-16 19:53:50
from src.utils.HTMLTestReportCN import HTMLTestRunner
from src.utils.mail import Email
from src.utils.config import Config,DATA_PATH,REPORT_PATH
import time,sys,os
import unittest
from src.utils.excel_write import writeExcel
from src.utils.DBoperator import MYSQL,MyRedis

class RunAllTests(object):
	""""""
	def __init__(self):
		self.test_case_path = os.path.join(os.getcwd(),"src/test/interface")
		self.title = '开放平台接口测试报告'
		self.description = 'AutoReport'
		self.host = Config().get('OpenPlatform_API').get('DATABASE').get('host')
		self.username = Config().get('OpenPlatform_API').get('DATABASE').get('username')
		self.pwd = Config().get('OpenPlatform_API').get('DATABASE').get('password')
		self.dbname1 = Config().get('OpenPlatform_API').get('DATABASE').get('database_merchant')
		self.dbname2 = Config().get('OpenPlatform_API').get('DATABASE').get('database_player')
		self.dbname3 = Config().get('OpenPlatform_API').get('DATABASE').get('database_redeemmall')

	def init_data(self):
		self.retaintable = Config().get('OpenPlatform_API').get('DATABASE').get('retaintable')
		self.redis_host = Config().get('OpenPlatform_API').get('Redis').get('host')
		self.clearkeys_player = Config().get('OpenPlatform_API').get('Redis').get('clearkeys_player')
		self.clearkeys_merchant = Config().get('OpenPlatform_API').get('Redis').get('clearkeys_merchant')
		db_merchant = MYSQL(host=self.host, user=self.username ,pwd=self.pwd, dbname=self.dbname1)
		db_player = MYSQL(host=self.host, user=self.username ,pwd=self.pwd, dbname=self.dbname2)
		db_redeemmall = MYSQL(host=self.host, user=self.username ,pwd=self.pwd, dbname=self.dbname3)
		redis_merchant = MyRedis(ip=self.redis_host,db=1)
		redis_player = MyRedis(ip=self.redis_host,db=0)
		
		#清理商户数据库以及对应的redis,并插入测试基础数据
		TableList1 = db_merchant.query(sql='show tables',datasize=0)[0]
		db_merchant.db_clear(tablename='Channel')
		db_merchant.db_clear(tablename='Template')
		for i in (item[key] for item in TableList1 for key in item if item[key] not in self.retaintable):
			# print(i)
			db_merchant.db_clear(tablename=i)
		for key in self.clearkeys_merchant.split(','):
			redis_merchant.clear_anykeys(pattern=key)

		sql = DATA_PATH + '/basedata_merchant.sql'
		with open(sql, 'r+',encoding='UTF-8') as sql:
			sql_list = sql.read().split(';')[:-1]  # sql文件最后一行加上;
			sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
		for sql_item  in sql_list:
			db_merchant.cur.execute(sql_item)
			db_merchant.conn.commit()
		db_merchant.cur.close()
		db_merchant.conn.close()

		#清理玩家数据库及对应的redis,并插入测试基础数据
		TableList2 = db_player.query(sql='show tables',datasize=0)[0]
		for i in (item[key] for item in TableList2 for key in item if item[key] not in self.retaintable):
			db_player.db_clear(tablename=i)
		for key in self.clearkeys_player.split(','):
			redis_player.clear_anykeys(pattern=key)

		sql = DATA_PATH + '/basedata_player.sql'
		with open(sql, 'r+',encoding='UTF-8') as sql:
			sql_list = sql.read().split(';')[:-1]  # sql文件最后一行加上;
			sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
		for sql_item  in sql_list:
			db_player.cur.execute(sql_item)
			db_player.conn.commit()
		db_player.cur.close()
		db_player.conn.close()

		#清理兑换商城数据库及对应的redis,并插入测试基础数据
		TableList3 = db_redeemmall.query(sql='show tables',datasize=0)[0]
		for i in (item[key] for item in TableList3 for key in item if item[key] not in self.retaintable):
			db_redeemmall.db_clear(tablename=i)
		# for key in self.clearkeys_redeemmall.split(','):
		# 	redis_redeemmall.clear_anykeys(pattern=key)

		sql = DATA_PATH + '/basedata_redeemmall.sql'
		with open(sql, 'r+',encoding='UTF-8') as sql:
			sql_list = sql.read().split(';')[:-1]  # sql文件最后一行加上;
			sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
		for sql_item  in sql_list:
			db_redeemmall.cur.execute(sql_item)
			db_redeemmall.conn.commit()
		db_redeemmall.cur.close()
		db_redeemmall.conn.close()
	 
	def run(self):

		self.init_data()

		suite = unittest.TestLoader().discover(self.test_case_path)

		report_path = os.path.join(REPORT_PATH , 'report.html')

		# resultpath = os.path.join(REPORT_PATH , 'report.xlsx')
		# resultdata= list()
		# resultdata.insert(0,["用例编号","用例名称","请求数据","预期结果","返回结果"])

		with open(report_path, 'wb') as f:
			runner = HTMLTestRunner(f, title=self.title, description=self.description, tester='web测试组')
			runner.run(suite)
		# writeExcel(path=resultpath, data=resultdata)
		# 发送邮件
		# e = Email(title = Config().get('email').get('title'),
  #             message = Config().get('email').get('message'),
  #             receiver = Config().get('email').get('receiver'),
  #             server = Config().get('email').get('server'),
  #             sender = Config().get('email').get('sender'),
  #             password = Config().get('email').get('password'),
  #             path = report_path
  #             )
		# e.send()

if __name__ == '__main__':
	RunAllTests().run()
	#取当前时间
	# now= time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
	# report = os.path.join(REPORT_PATH , now + 'report.html')
	# resultpath = os.path.join(REPORT_PATH , now + 'report.xlsx')
	# report = os.path.join(REPORT_PATH , 'report.html')
	# resultpath = os.path.join(REPORT_PATH , 'report.xlsx')
	# resultdata= list()
	# resultdata.insert(0,["用例编号","用例名称","预期结果","返回结果"])
	# allsuite = allCase()
	# suite = unittest.TestSuite()
	# suite.addTest(TestMerchant('test_CreateMerchant'))
	# suite.addTest(TestMerchant('test_EditMerchant'))
	# suite.addTest(TestMerchant('test_GetMerchant'))
	# suite.addTest(TestMerchant('test_MerchantList'))
	# with open(report, 'wb') as f:
	# 	runner = HTMLTestRunner(f, verbosity=2, title='开放平台接口测试报告', description='',tester='web测试组')
	# 	runner.run(allsuite)
	# writeExcel(path=resultpath, data=resultdata)
