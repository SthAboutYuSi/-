# -*- coding: utf-8 -*-
# @Author: yusi
# @Date:   2019-07-17 10:16:49
# @Last Modified by:   yusi
# @Last Modified time: 2019-07-23 14:51:04
"""抽取器，从响应结果中抽取部分数据"""

import json
import jmespath


class JMESPathExtractor(object):
    """
    用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self, query=None, body=None):
        try:
            return jmespath.search(query, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))

if __name__ == '__main__':
	s ='{"success": true,"error": null,"responseTime": "2019-07-23 10:57:39.498","data": {"data": [{"id": "39ef2ee4e796add36b93cdde2ccfdb77","name": "中顺网络公司","shortName": "ZS棋牌","code": "A0016587","type": 1,"typeName": "自研","state": 1,"stateName": "正常"}],"recordsTotal": 1}}'
	a=JMESPathExtractor().extract(query='data.data[0].id', body=s)
	print (a)
