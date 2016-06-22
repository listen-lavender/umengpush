#!/usr/bin/env python
# coding=utf8

from . import UmengPush, shallow_check

def merge(src, obj):
    for key in src:
        obj[key] = src[key]

class UmengIosPush(UmengPush):

    _body_tpl = {
        "alert": True,
        "badge": True,
        "sound": True,
        "content-available": True,
        "category": True,
    }

    _policy_tpl = {
        "start_time": True,
        "expire_time": True,
        "max_send_num": True,
    }

    def directedcast(self, device_token, body, display_type='notification', extra={}, policy={}, description=""):
        if type(device_token) == str:
            device_token = [device_token, ]
        if len(device_token) > 500:
            raise Exception("Token不能超过500个，请选择filecast")
        for item in device_token:
            if not len(item) == 64:
                raise Exception("Token %s is not right.")
        if len(device_token) == 1:
            self.type = 'unicast'
        else:
            self.type = 'listcast'
        self.device_token = ','.join(device_token)
        self.description = description

        payload = {'aps':body}
        shallow_check(payload['aps'], self._body_tpl)
        merge(extra, payload)

        return self.send(payload, policy)

    def broadcast(self, body, display_type='notification', extra={}, policy={}, description=""):
        self.type = 'broadcast'
        self.description = description

        payload = {'aps':body}
        shallow_check(payload['aps'], self._body_tpl)
        merge(extra, payload)

        return self.send(payload, policy)

    def groupcast(self, condition, body, display_type, extra={}, policy={}, description=""):
        self.type = 'groupcast'
        self.description = description

        self.filter = {'where':condition}
        
        payload = {'aps':body}
        shallow_check(payload['aps'], self._body_tpl)
        merge(extra, payload)

        return self.send(payload, policy)

    def customizedcast(self, alias, alias_type, body, display_type, extra={}, policy={}, description=""):
        self.type = 'customizedcast'
        self.description = description

        if type(alias) == str:
            alias = [alias, ]
        if len(alias) > 50:
            raise Exception("Alias不能超过50个，请选择filecast")

        self.alias = alias
        self.alias_type = alias_type

        payload = {'aps':body}
        shallow_check(payload['aps'], self._body_tpl)
        merge(extra, payload)

        return self.send(payload, policy)

    def filecast(self, file_id, body, display_type, extra={}, policy={}, description=""):
        self.type = 'filecast'
        self.description = description

        self.file_id = file_id

        payload = {'aps':body}
        shallow_check(payload['aps'], self._body_tpl)
        merge(extra, payload)
        
        return self.send(payload, policy)


if __name__ == '__main__':
    pass
