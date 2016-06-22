#!/usr/bin/env python
# coding=utf8

from . import UmengPush, shallow_check

class UmengAndroidPush(UmengPush):

    _body_tpl = {
        "ticker": True,
        "title": True,
        "text": True,
        "icon": True,
        "largeIcon": True,
        "img": True,
        "sound": True,
        "builder_id": True,
        "play_vibrate": True,
        "play_lights": True,
        "play_sound": True,
        "after_open": True,
        "url": True,
        "activity": True,
        "custom": True,
    }

    _policy_tpl = {
        "start_time": True,
        "expire_time": True,
        "max_send_num": True,
        "out_biz_no": True,
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

        if display_type == 'notification':
            if (not body.get('ticker') or not body.get('title') or not body.get('text')):
                raise Exception("定向 notification 消息必须包含ticker, title, text.")
            if not body.get('after_open'):
                raise Exception("定向 notification 消息必须包含点击后续行为.")
            if body['after_open'] == 'go_url' and not body.get('url'):
                raise Exception("缺少点击跳转url.")
            if body['after_open'] == 'go_activity' and not body.get('activity'):
                raise Exception("缺少点击跳转activity.")
            if body['after_open'] == 'go_custom' and not body.get('custom'):
                raise Exception("缺少点击跳转自定义行为.")
        else:
            if not body.get('custom'):
                raise Exception("缺少透传消息内容.")

        payload = {'display_type':display_type, 'body':body, 'extra':extra}
        shallow_check(payload['body'], self._body_tpl)

        return self.send(payload, policy)

    def broadcast(self, body, display_type='notification', extra={}, policy={}, description=""):
        self.type = 'broadcast'
        self.description = description

        payload = {'display_type':display_type, 'body':body, 'extra':extra}
        shallow_check(payload['body'], self._body_tpl)

        return self.send(payload, policy)

    def groupcast(self, condition, body, display_type, extra={}, policy={}, description=""):
        self.type = 'groupcast'
        self.description = description

        self.filter = {'where':condition}
        
        payload = {'display_type':display_type, 'body':body, 'extra':extra}
        shallow_check(payload['body'], self._body_tpl)

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

        payload = {'display_type':display_type, 'body':body, 'extra':extra}
        shallow_check(payload['body'], self._body_tpl)

        return self.send(payload, policy)

    def filecast(self, file_id, body, display_type, extra={}, policy={}, description=""):
        self.type = 'filecast'
        self.description = description

        self.file_id = file_id

        payload = {'display_type':display_type, 'body':body, 'extra':extra}
        shallow_check(payload['body'], self._body_tpl)

        return self.send(payload, policy)


if __name__ == '__main__':
    pass
