# encoding:utf-8
# @CreateTime: 2022/9/19 11:50
# @Author: Xuguangchun
# @FlieName: test_OpenSea.py
# @SoftWare: PyCharm
import json

import requests

url = "https://api.opensea.io/api/v1/collection/emoheads/stats"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(json.dumps(json.loads(response.text),indent=4))