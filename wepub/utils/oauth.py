#!/usr/bin/env python
# encoding: utf-8

from tornado.httpclient import HTTPClient
from tornado.escape import json_decode


def get_client_id_and_secret():
    # TODO: 挪到配置文件
    url = 'https://login.lecloud.com/nopagelogin?username=matrix&password=matrix'
    response = HTTPClient().fetch(url)
    return json_decode(response.body)
