#!/usr/bin/env python
# encoding: utf-8

from tornado.escape import json_decode

from wepub.common import RESTfulHandler
from wepub.models.node import Node, NodeGroup


class NodeHandler(RESTfulHandler):
    """
    处理客户端对Node资源发出的HTTP请求
    """

    def create(self):
        """
        HTTP 方法: POST

        在数据库中新增一条Node数据，若创建Node成功则返回状态码201，
        创建失败则返回400，遇到内部错误返回500.
        """
        appdata = json_decode(self.request.body)
        app = Node(**appdata)
        app.create()

    def gets(self, appid):
        """
        HTTP 方法: GET

        客户端根据appid读取一条Node数据，若正常返回200和Node数据，若
        根据该appid未找到数据则返回404，内部错误返回500.
        """
        pass

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明appid时，返回所有Node信息，需考虑分页
        """
        pass

    def update(self, appid):
        """
        HTTP 方法: PUT

        根据appid全量更新一条Node数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有Node数据, 批量更新
        """
        pass

    def delete(self, appid):
        """
        HTTP 方法: DELETE

        根据appid删除一条Node数据，可以物理删除或逻辑删除，删除后再被GET请求
        时应报错404。
        """
        pass

    def delete_collection(self):
        """
        HTTP 方法: DELETE

        删除所有Node数据，批量删除
        """
        pass


class NodeGroupHandler(RESTfulHandler):
    """
    处理客户端对NodeGroup资源发出的HTTP请求
    """

    def create(self):
        """
        HTTP 方法: POST

        在数据库中新增一条NodeGroup数据，若创建NodeGroup成功则返回状态码201，
        创建失败则返回400，遇到内部错误返回500.
        """
        appdata = json_decode(self.request.body)
        app = NodeGroup(**appdata)
        app.create()

    def gets(self, appid):
        """
        HTTP 方法: GET

        客户端根据appid读取一条NodeGroup数据，若正常返回200和NodeGroup数据，若
        根据该appid未找到数据则返回404，内部错误返回500.
        """
        pass

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明appid时，返回所有NodeGroup信息，需考虑分页
        """
        pass

    def update(self, appid):
        """
        HTTP 方法: PUT

        根据appid全量更新一条NodeGroup数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有NodeGroup数据, 批量更新
        """
        pass

    def delete(self, appid):
        """
        HTTP 方法: DELETE

        根据appid删除一条NodeGroup数据，可以物理删除或逻辑删除，删除后再被GET请求
        时应报错404。
        """
        pass

    def delete_collection(self):
        """
        HTTP 方法: DELETE

        删除所有NodeGroup数据，批量删除
        """
        pass
