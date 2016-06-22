#!/usr/bin/env python
# coding=utf8
from abc import abstractmethod
import json
import hashlib
import requests
import time

APP_KEY = '#'
APP_SECRET = '#'

def timestamp():
    return int(time.time()*1000)

def serialize(data):
    return json.loads(data)

def unserialize(data):
    return json.dumps(data, ensure_ascii=False, encoding='utf8', sort_keys=True).encode('utf-8')

def sign(url, data, key):
    return hashlib.md5('%s%s%s%s'%('POST', url, data, key)).hexdigest()

def shallow_check(obj, src):
    for key in obj:
        if src.get(key):
            pass
        else:
            raise Exception("Key %s is not in (%s)." % (key, ','.join(src.keys())))

def deep_check(obj, src, operators={}):
    for key in obj:
        val = obj[key]
        if operators.get(key):
            if isinstance(val, dict):
                deep_check(val, src, operators=operators)
            else:
                raise Exception("No right condition for operator %s." % operators[key])
        elif src.get(key):
            pass
        else:
            raise Exception("Key %s is not in (%s)." % (key, ','.join(src.keys())))

class UmengPush(object):
    """
        appkey：应用唯一标识。
        友盟消息推送服务提供的appkey
        和友盟统计分析平台使用的同一套appkey。

        app_master_secret：服务器秘钥，
        用于服务器端调用API，
        请求时对发送内容做签名验证。

        production_mode: 正式/测试模式。
        测试模式下，广播/组播只会将消息发给测试设备。
        测试设备需要到web上添加。
        Android测试设备属于正式设备的一个子集。

        thirdparty_id: 开发者自定义消息标识ID, 
        开发者可以为同一批发送的多条消息。
    """
    PRODUCTION_MODE = 'true'
    _filter_tpl = {"app_version": True,
        "channel": True,
        "device_model": True,
        "province": True,
        "tag": True,
        "country": True,
        "language": True,
        "launch_from": True,
        "not_launch_from": True,
    }
    _filter_operator = {'and': True, 
        'or': True,
        'not': True}
    _send_url = '/api/send'
    _upload_url = '/api/upload'

    def __init__(self, appkey=APP_KEY, appsecret=APP_SECRET, thirdparty=None, host='http://msg.umeng.com'):
        self.host = host
        self.appkey = appkey
        self.appsecret = appsecret
        self.thirdparty = thirdparty
        self.type = ''
        self.description = ''
        self.device_token = ''
        self.filter = {}
        self.alias = ''
        self.alias_type = ''
        self.file_id = ''

    def send(self, payload, policy={}):

        data = {
            'appkey': self.appkey,
            'payload': payload,
            'type': self.type,
            'production_mode': self.PRODUCTION_MODE,
            'timestamp': timestamp(),
        }
        if self.description:
            data['description'] = self.description

        if self.device_token:
            data['device_tokens'] = self.device_token
        if self.filter:
            deep_check(self.filter['where'], self._filter_tpl)
            data['filter'] = self.filter
        if self.alias and self.alias_type:
            data['alias'] = self.alias
            data['alias_type'] = self.alias_type
        if self.file_id:
            data['file_id'] = self.file_id

        if policy:
            shallow_check(policy, self._policy_tpl)
            data['policy'] = policy

        if self.thirdparty:
            data['thirdparty'] = self.thirdparty

        data = unserialize(data)
        signature = sign('%s%s' % (self.host, self._send_url), data, self.appsecret)
        result = requests.post(('%s%s?sign=%s') % (self.host, self._send_url, signature), data=data)
        print ('%s%s?sign=%s') % (self.host, self._send_url, signature)
        print data
        return serialize(result.content)
    
    @abstractmethod
    def directedcast(self, device_token, body, display_type='notification', extra={}, policy={}, description=""):
        """
            定向消息: 向指定的设备发送消息，
            包括单播(unicast) or 列播(listcast)
            向若干个device_token或者若干个alias发消息。
        """
        # self.delegator.directedcast(device_token, body, display_type=display_type, extra=extra, policy=policy, description=description)
        pass
    
    @abstractmethod
    def broadcast(self, body, display_type='notification', extra={}, policy={}, description=""):
        """
            广播消息(broadcast，属于task): 向安装该App的所有设备发送消息。
        """
        # self.delegator.broadcast(body, display_type=display_type, extra=extra, policy=policy, description=description)
        pass
    
    @abstractmethod
    def groupcast(self, condition, body, display_type, extra={}, policy={}, description=""):
        """
            组播消息(groupcast，属于task): 向满足特定条件的设备集合发送消息，
            例如: "特定版本"、"特定地域"等。
            友盟消息推送所支持的维度筛选
            和友盟统计分析所提供的数据展示维度是一致的，
            后台数据也是打通的
        """
        # self.delegator.groupcast(condition, body, display_type=display_type, extra=extra, policy=policy, description=description)
        pass
    
    @abstractmethod
    def customizedcast(self, alias, alias_type, body, display_type, extra={}, policy={}, description=""):
        """
            自定义消息(customizedcast，属于task): 开发者通过自有的alias进行推送, 
            可以针对单个或者一批alias进行推送，
            也可以将alias存放到文件进行发送。
        """
        # self.delegator.customizedcast(alias, alias_type, body, display_type=display_type, extra=extra, policy=policy, description=description)
        pass
    
    @abstractmethod
    def filecast(self, file_id, body, display_type, extra={}, policy={}, description=""):
        """
            文件消息(filecast，属于task)：开发者将批量的device_token
            或者alias存放到文件, 通过文件ID进行消息发送。
        """
        # self.delegator.filecast(file_id, body, display_type=display_type, extra=extra, policy=policy, description=description)
        pass

    def upload_file(self, content):
        """ content 由device_token组成或者alias组成，\n隔开
        """
        data = {
            'appkey': self.appkey,
            'timestamp': timestamp(),
            'content': content
        }
        data = unserialize(data)
        signature = sign('%s%s' % (self.host, self._upload_url), data, self.appsecret)
        result = requests.post(('%s%s?sign=%s') % (self.host, self._upload_url, signature), data=data)
        return serialize(result.content)['data']['file_id']


if __name__ == '__main__':
    pass
