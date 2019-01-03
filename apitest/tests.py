# from django.test import TestCase
import requests
import time
import json
import logging
from apitest.models import Apis, Apiinfo

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
if 1:
    logging.disable(logging.DEBUG)

# 登陆信息
loginApi = {
    'name': '用户登陆',
    'method': 'post',
    'url': 'https://www.wukoon-app.com/api/v1/user/login',
    'param': None,
    'json': {
        'email': '18129832245@163.com',
        'pswmd5': '202cb962ac59075b964b07152d234b70',
        'timestamp': int(time.time())
    },
    'response': {
        'errcode': 0,
        'errmsg': 'ok'
    }
}

TOKEN = ''


# 登陆
def login():
    api = loginApi
    start = time.time()
    r = requests.Response()
    error = 'PASS'
    try:
        r = requests.request(
            method=api['method'],
            url=api['url'],
            params=api['param'],
            json=api['json'])
    except requests.exceptions.ConnectionError:
        error = "ConnectionError"
    except requests.exceptions.HTTPError:
        error = "HTTPError"
    except requests.exceptions.URLRequired:
        error = "URLRequired"
    except requests.exceptions.TooManyRedirects:
        error = "TooManyRedirects"
    except requests.exceptions.ReadTimeout:
        error = "ReadTimeout"
    except requests.exceptions.InvalidURL:
        error = "InvalidURL"

    finally:
        if error != 'PASS':
            return False
    # 计算测试时间，精确到小数点后两位
    timeval = time.time() - start
    timeval = str(round(timeval, 2))
    logging.debug('RESPONSE：' + r.text)
    rev = json.loads(r.text)
    if 'data' in rev:
        if 'token' in rev['data']:
            global TOKEN
            TOKEN = rev['data']['token']
    if rev['errcode'] == api['response']['errcode'] and rev['errmsg'] == api[
            'response']['errmsg']:
        logging.info(error + '-' + api['name'] + ' 测试时间：' + timeval)
    else:
        error = 'FAIL-RESPONSE 不一致'
        logging.info(error + '-' + api['name'] + '-测试时间：' + timeval)
    return r.text


# 测试API
def test_apis():
    login()
    apis = Apis.objects.all()
    for api in apis:
        # 预设为True
        api.apistatus = True
        apiinfos = Apiinfo.objects.filter(api=api)
        for apiinfo in apiinfos:
            apitest = {}
            apitest['name'] = apiinfo.apiname
            apitest['method'] = apiinfo.apimethod
            apitest['url'] = api.apiurl + apiinfo.apiurl

            if apiinfo.apiparamvalue:
                apitest['param'] = json.loads(apiinfo.apiparamvalue)
                if 'token' in apitest['param'] and TOKEN != '':
                    apitest['param']['token'] = TOKEN
                    apiinfo.apiparamvalue = json.dumps(apitest['param'])
            else:
                apitest['param'] = apiinfo.apiparamvalue

            if apiinfo.apijson:
                apitest['json'] = json.loads(apiinfo.apijson)
                if 'timestamp' in apitest['json']:
                    apitest['json']['timestamp'] = int(time.time())
            else:
                apitest['json'] = apiinfo.apijson
            apitest['response'] = json.loads(apiinfo.apiresponse)
            logging.debug(apitest)
            # url请求测试
            result = api_request(apitest)
            apiinfo.apistatus = result
            apiinfo.save()
            api.apistatus = (result and api.apistatus)
        api.save()


# 测试请求
def api_request(api):
    start = time.time()
    r = requests.Response()
    error = 'PASS'
    try:
        r = requests.request(
            method=api['method'],
            url=api['url'],
            params=api['param'],
            json=api['json'])
    except requests.exceptions.ConnectionError:
        error = "ConnectionError"
    except requests.exceptions.HTTPError:
        error = "HTTPError"
    except requests.exceptions.URLRequired:
        error = "URLRequired"
    except requests.exceptions.TooManyRedirects:
        error = "TooManyRedirects"
    except requests.exceptions.ReadTimeout:
        error = "ReadTimeout"
    except requests.exceptions.InvalidURL:
        error = "InvalidURL"

    finally:
        if error != 'PASS':
            return False
    # 计算测试时间，精确到小数点后两位
    timeval = time.time() - start
    timeval = str(round(timeval, 2))
    logging.debug('RESPONSE：' + r.text)
    rev = json.loads(r.text)
    if 'data' in rev:
        if 'token' in rev['data']:
            global TOKEN
            TOKEN = rev['data']['token']
    if rev['errcode'] == api['response']['errcode'] and rev['errmsg'] == api[
            'response']['errmsg']:
        logging.info(error + '-' + api['name'] + ' 测试时间：' + timeval)
        return True
    else:
        error = 'FAIL-RESPONSE 不一致'
        logging.info(error + '-' + api['name'] + '-测试时间：' + timeval)
        return False
