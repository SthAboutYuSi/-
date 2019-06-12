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

# if __name__ == '__main__':
# 	a=JMESPathExtractor().extract(query='ret', body='{"ret":-2}')
# 	print (a)
