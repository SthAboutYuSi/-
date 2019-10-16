import  pymysql,redis
import  sys,os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from src.utils.config import Config,DATA_PATH,REPORT_PATH
from src.utils.log import logger
# from src.utils.config import Config
  
class MYSQL(object):  
    '''
    定义对mysql数据库基本操作的封装
    ''' 
    def __init__(self,host,user,pwd,dbname=None,port=3306,charset='utf8'):  
        '''
        初始化函数，初始化连接列表 
        :param host:数据库服务器地址
        :param port数据库服务器端口号
        :param user:数据库用户名
        :param pwd:用户的密码
        :param dbname:要操作的库名称
        '''
        self.host = host
        self.user = user  
        self.passwd  = pwd  
        self.db= dbname
        self.port = port
        self.charset = charset
    
        try:
            # 建立数据库连接  
            self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)  
        except ConnectionError as e:
            logger.debug("Mysql Error %d: %s" % (e.args[0],e.args[1]))
        # 创建游标对象:用于执行查询和获取结果 
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def __enter__(self):
    # 返回游标
        return self.cur
 
    def __exit__(self, exc_type, exc_val, exc_tb):
    # 提交数据库并执行
        self.conn.commit()
    # 关闭游标
        self.cur.close()
    # 关闭数据库连接
        self.conn.close()

  
    # 查询操作  
    def query(self,sql, params=None, datasize=1):
        self.datasize = datasize 
        """
        参数sql：包含%s的sql字符串，当params=None的时候，不包含%s
        参数params：一个元祖，默认为None
        参数datasize：0-返回所有结果   1-每次返回一条结果   n-每次返回n条结果
        """ 
        try:
            # 执行SQL语句  
            self.cur.execute(sql, params)
            # 获取数据的行数  
            row = self.cur.rowcount 
            # 获取查询数据  
            """
            cursor.fetchone()：将只取最上面的第一条结果，返回单个元组如('id','title')，然后多次使用cursor.fetchone()，依次取得下一条结果，直到为空。
            cursor.fetchall() :将返回所有结果，返回二维元组，如(('id','title'),('id','title'))
            cursor.fetchmany(n):每次抓取n条记录，该方法返回一个由n条记录组成的列表
            """ 
            if self.datasize == 1:
                dataList = self.cur.fetchone()
            elif self.datasize == 0:
                dataList = self.cur.fetchall()
            else: 
                dataList = self.cur.fetchmany(self.datasize)
        except:
            logger.error("Error: unable to fetch data")  
   
        return dataList,row 
  
    def operation(self,sql,params=None):
        '''
        单条数据的操作，insert，update，delete
        :param sql:包含%s的sql字符串，当params=None的时候，不包含%s
        :param params:一个元祖，默认为None
        :return:如果执行过程没有crash，返回True，反之返回False
        '''
        try:  
            # 执行SQL语句  
            self.cur.execute(sql, params)  
            # 正常结束事务  
            self.conn.commit()
            return True 
        except Exception as e:
            # 数据库回滚  
            self.conn.rollback()   
            logger.info("[sql_str_message]-%s" %cur.mogrify(sql, params))
            logger.exception(e)
            return False

    def db_insert(self, table_name, table_data):
        """插入多条数据"""
        
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        # print(type(value))
        # print(value.split(',')[0])
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        
        logger.info('执行SQL语句%s' %real_sql)
        self.cur.execute(real_sql)
        self.conn.commit() 

    def db_clear(self, tablename):
        """清除表数据"""
        sql = "truncate table %s;" % tablename
        self.cur.execute(sql)
        logger.info("清理%s库中的数据表%s数据" % (self.db,tablename)) 
        self.conn.commit()

    # def init_data(self, datas):
    #     """初始化数据"""
    #     for table, data in datas.items():
    #         self.clear(table)
    #         for d in data:
    #             self.db_insert(table, d)

class MyRedis():
    def __init__(self,ip,password=None,port=6379,db=0):
        #构造函数
        try:
            self.r = redis.Redis(host=ip,password=password,port=port,db=db)
            # r = redis.ConnectionPool(host=ip,password=password,port=port,db=db)
        except Exception as e:
            logger.error('redis连接失败，错误信息%s'%e)

    def str_get(self,k):
        res = self.r.get(k)
        if res:
            return res.decode()#获取数据要有返回值，所以要有返回值

    def str_set(self,k,v,time=None):
        self.r.set(k,v,time)

    def delete(self,k):
        tag = self.r.exists(k) #判断这个key是否存在
        if tag:
            self.r.delete(k)
            logger.info('%s删除成功' %k)
        else:
            logger.info('这个key%s不存在' %k)

    def hash_get(self,name,k): #无论key是否存在，都不会报错，所以不用写try
        res = self.r.hget(name,k)
        if res:
            return res.decode()

    def hash_set(self,name,k,v):
        self.r.hset(name,k,v)

    def hash_getall(self,name):
        data = {}
        # {b'12': b'1212', b'3': b'sdad', b'4': b'asdadsa'}
        res = self.r.hgetall(name)
        if res:
            for k,v in res.items():
                k =  k.decode()
                v = v.decode()
                data[k]=v
        return data

    def hash_del(self,name,k):
        res = self.r.hdel(name,k)
        if res:#因为删除成功会返回1，删除失败返回0
            logger.info('删除成功')
            return 1
        else:
            logger.info('删除失败，该key不存在')
            return 0

    @property#定义为属性方法，以后可以直接调用
    def clean_redis(self):
        self.r.flushdb()  #清1空redis
        logger.info('清空redis成功！')
        return 0

    def clear_anykeys(self,pattern):
        keys=self.r.keys(pattern=pattern)
        if len(keys)==0:
            logger.info('没有查询到匹配%s的key值' %pattern)
        else:
            self.r.delete(*keys)
            logger.info('匹配%s的key值清除成功' %pattern)
        


if __name__ == '__main__':
    # host = Config().get('OpenPlatform_API').get('DATABASE').get('host')
    # username = Config().get('OpenPlatform_API').get('DATABASE').get('username')
    # pwd = Config().get('OpenPlatform_API').get('DATABASE').get('password')
    # dbname1 = Config().get('OpenPlatform_API').get('DATABASE').get('database_merchant')
    # dbname2 = Config().get('OpenPlatform_API').get('DATABASE').get('database_player')
    # # retaintable = Config().get('OpenPlatform_API').get('DATABASE').get('retaintable')
    # db_merchant = MYSQL(host=host, user=username ,pwd=pwd, dbname=dbname1)
    # # s=db_merchant.query('select * from ChannelSubpackage;')
    # # print(s)
    # db_player = MYSQL(host=host, user=username ,pwd=pwd, dbname=dbname2)
    # # sql = "select playerid from Player where PlayerAccount='Ut7C80JFuu' or PlayerAccount='wWSsR9t2jA';"
    # # TableList = db_merchant.query(sql='show tables',datasize=0)[0]
    # # from data import basedata
    # # for tbname,data in basedata.playerdatas.items():
    # #     for d in data:
    # #         if tbname == 'PlayerQuestionAnswers':               
    # sql = DATA_PATH + '/basedata_player.sql'
    # with open(sql, 'r+') as sql:
    #     sql_list = sql.read().split(';')[:-1]  # sql文件最后一行加上;
    #     sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
    # for sql_item  in sql_list:
    #     db_player.cur.execute(sql_item)
    #     db_player.conn.commit()
    #     print(sql_item)
    # clearkeys=Config().get('OpenPlatform_API').get('Redis').get('clearkeys_merchant')
    # print (clearkeys)
    # for key in clearkeys.split(','):
    # #         keys = redis.Redis(host='10.8.26.230',db=1).keys(pattern=key)
    #         print (key)
    # s=MyRedis(ip='10.8.26.230').clear_anykeys(pattern='OpenPlatform:PlayerCenter:FindPlayerIdByAccount:xu6c0a61O*')
    # a=MyRedis(ip='10.8.26.230').str_get('OpenPlatform:PlayerCenter:FindPlayerIdByAccount:xu6c0a61O')
    # print(s)
   value="'39ef7c15c92500267d3ef9200615525b','39ef7c159eeccd86e6bf71e539bffc9f','81026965001','null','1','1','1','1','0'"
   print(int(value.split(',')[4][1]))
   # for v in value.split(','):
   #      print(v)
   #      v.replace('\"','')
   #      if v== "'1'":

   #          v=int(v)
   #      print(v,type(v))

   # a=(int(value.split(',')[4]))
   # print(a)