"""
添加用于接口测试的client，对于HTTP接口添加HTTPClient，发送http请求。
还可以封装TCPClient，用来进行tcp链接，测试socket接口等等。
"""

import requests,sys,os,json

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from src.utils.log import logger
from src.utils.extractor import JMESPathExtractor

METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']


class UnSupportMethodException(Exception):
    """当传入的method的参数不是支持的类型时抛出此异常。"""
    pass


class HTTPClient(object):
    """
    http请求的client。初始化时传入url、method等，可以添加headers和cookies，但没有auth、proxy。

    >>> HTTPClient('http://www.baidu.com').send()
    <Response [200]>

    """
    def __init__(self, url, method='GET', headers=None, cookies=None):
        """headers: 字典。 例：headers={'Content_Type':'text/html'}，cookies也是字典。"""
        self.url = url
        self.session = requests.session()
        self.method = method.upper()
        if self.method not in METHODS:
            raise UnSupportMethodException('不支持的method:{0}，请检查传入参数！'.format(self.method))

        self.set_headers(headers)
        self.set_cookies(cookies)

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self, params=None, data=None, **kwargs):
        response = self.session.request(method=self.method, url=self.url, params=params, data=data, **kwargs)
        response.encoding = 'utf-8'
        logger.debug('params:{0}, data:{1}'.format(params, data))
        logger.debug('{0} {1}'.format(self.method, self.url))
        if response.status_code == 200:
            logger.debug('请求成功: {0}\n{1}'.format(response, response.text))
        else:
            logger.debug('请求失败：{0}\n{1}'.format(response, response.text))
        return response

if __name__ == '__main__':
    datas="{'mchId': 10001, 'isPloy': 0, 'platformType': 1, 'userID': 10087, 'account': 10087, 'orderNO': '155929124913961877', 'productId': 101, 'channelNO': 1020001001, 'payAmount': 6, 'itemID': 10001, 'itemCount': 50001, 'subject': '6W', 'body': '6W', 'device': 0, 'method': 0, 'gateway': 101, 'identity': 'r0tv6alf3c6eo8rfa5df85j8kg0mtach', 'extData1': '', 'payExtInfo': '', 'sign': '', 'signType': 'RSA', 'version': '1.0'}"
    
    url = "http://10.8.26.218:1029/pay"
    headers={
    'Content-Type': "application/json"


    
   
    
   
   
    }
    # # print (len(datas))
    # # requests.session().headers.update({'content-type': 'application/json'})
    # print (requests.session().headers)
    # for d in range(0,len(datas)):
    #     print (datas[d])
        # print (str(json.dumps(datas[d])))
    #     # print (type(datas[d]))
        # res = HTTPClient(url='http://10.8.26.218:1029/pay', method='POST', headers={'Content_Type':'application/json'}).send(data=datas[d])
    response = requests.request("POST",url, data=datas, headers={'Content-Type': "application/json"})

    #     print (len(res.text))
    #     print (type(res.text))
    print (response)
    #     a = JMESPathExtractor().extract(query='[0].itemName', body=res.text)
    #     # a= json.loads(res.text)
    #     print (type(a))
    #     print (a)
    #     # print (a[0]['itemName'])
    # datas = {"type":"user_mail_operation","operation":1,"id":317,"to":["321245","321303","321304"],"title":"接口测试33","contain":"接口测试","time":1553581757,"reward":""}
    # res = HTTPClient(url='http://10.8.12.169/game_master/game_master.php', method='POST').send(json=datas)
    # print (res.text)