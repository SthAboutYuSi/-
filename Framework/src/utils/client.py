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

    datas = [{'productType': 2, 'currentPage': 3, 'pageSize': 2}]

    # print (len(datas))
    # requests.session().headers.update({'content-type': 'application/json'})
    print (requests.session().headers)
    for d in range(0,len(datas)):
        print (datas[d])
        # print (type(datas[d]))
        res = HTTPClient(url='http://wupdate.qkagame.net/api/Mall/Product/List', method='POST').send(data=datas[d])
        print (len(res.text))
        print (type(res.text))
        print (res.text)
        a = JMESPathExtractor().extract(query='[0].itemName', body=res.text)
        # a= json.loads(res.text)
        print (type(a))
        print (a)
        # print (a[0]['itemName'])