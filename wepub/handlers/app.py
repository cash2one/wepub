#!/usr/bin/env python
# encoding: utf-8

from tornado.escape import json_decode

from wepub.common import RESTfulHandler
from wepub.models.app import App


class AppHandler(RESTfulHandler):
    """
    处理客户端对App资源发出的HTTP请求
    """

    def create(self):
        """
        HTTP 方法: POST

        在数据库中新增一条App数据，若创建App成功则返回状态码201，
        创建失败则返回400，遇到内部错误返回500.
        """
        appdata = json_decode(self.request.body)
        app = App(**appdata)
        app.create()

    def gets(self, appid):
        """
        HTTP 方法: GET

        客户端根据appid读取一条App数据，若正常返回200和App数据，若
        根据该appid未找到数据则返回404，内部错误返回500.
        """
        pass

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明appid时，返回所有App信息，需考虑分页
        """
        pass

    def update(self, appid):
        """
        HTTP 方法: PUT

        根据appid全量更新一条App数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有App数据, 批量更新
        """
        pass

    def delete(self, appid):
        """
        HTTP 方法: DELETE

        根据appid删除一条App数据，可以物理删除或逻辑删除，删除后再被GET请求
        时应报错404。
        """
        pass

    def delete_collection(self):
        """
        HTTP 方法: DELETE

        删除所有App数据，批量删除
        """
        pass
