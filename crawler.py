# -*- coding: utf8 -*-

import requests
import json
import os

# 登录极客时间, 从cookie里找到这两个东西，配置一下
GCID = ''
GCESS = ''

# 保存路径
try:
    os.makedirs('./ppt/')
except:
    pass

# COOKIE
cookies = {'GCID': GCID, 'GCESS': GCESS}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Origin': 'https://ppt.geekbang.org',
}

# 列表页
list_resp = requests.post('https://ppt.geekbang.org/serv/ppt/list', json = {'conid': 28}, cookies = cookies, headers = headers)
list_resp  = json.loads(list_resp.text)
for lec in list_resp['data']['lectures'].values():
    if 'pptid' not in lec:
        continue

    download_req = {'conid': 28, 'pptid': lec['pptid']}
    # 下载页
    download_resp = requests.post('https://ppt.geekbang.org/serv/ppt/download', json = download_req, cookies = cookies, headers = headers)
    download_resp = json.loads(download_resp.text)

    # 下载
    file = './ppt/' + lec['title'] + '.pdf'
    try:
        dir = os.path.dirname(file)
        os.makedirs(dir)
    except:
        pass
    if not os.path.isfile(file):
        ppt_resp = requests.get(download_resp['data']['ppt_url'], cookies = cookies, headers = headers)
        with open(file, 'wb') as f:
            f.write(ppt_resp.content)
