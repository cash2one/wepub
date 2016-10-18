#!/usr/bin/env python
# encoding: utf-8


import logging
import traceback

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
        try:
            nodedata = json_decode(self.request.body)
            # when create an `Node` object, will automaticly save data to db
            node = Node(**nodedata)
            ret = node.valid_data
            self.set_status(201)
            logging.info("Create Node: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(400)
            logging.error("Create Node Error: %s" % ret)
        finally:
            self.finish(ret)

    def gets(self, nodeid):
        """
        HTTP 方法: GET

        客户端根据nodeid读取一条Node数据，若正常返回200和Node数据，若
        根据该nodeid未找到数据则返回404，内部错误返回500.
        """
        try:
            ret = Node.get_data_by_id(_id=nodeid)
            if ret is None:
                ret = {"status": 404, "message": "App Not Found!",
                       "nodeid": nodeid}
                self.set_status(404)
                logging.warning("Node Not Found: %s" % nodeid)
            else:
                self.set_status(200)
                logging.info("Query Node: %s, %s" % (nodeid, ret))
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get Node Error: %s, %s" % (nodeid, ret))
        finally:
            self.finish(ret)

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明nodeid时，返回所有Node信息，需考虑分页
        """
        try:
            ret = Node.all_data()
            if not ret:
                ret = {"status": 404, "message": "There has no Node!"}
                self.set_status(404)
                logging.warning("Node collection Not Found.")
            else:
                ret = {
                    'draw': 1,
                    'recordsTotal': len(ret),
                    'recordsFiltered': len(ret),
                    'data': ret
                }
                self.set_status(200)
                logging.info("Query Node collection: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get Node collection Error: %s" % ret)
        finally:
            self.finish(ret)

    def update(self, nodeid):
        """
        HTTP 方法: PUT

        根据nodeid全量更新一条Node数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有Node数据, 批量更新
        """
        pass

    def delete(self, nodeid):
        """
        HTTP 方法: DELETE

        根据nodeid删除一条Node数据，可以物理删除或逻辑删除，删除后再被GET请求
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
        try:
            ndgroupdata = json_decode(self.request.body)
            ndgroup = NodeGroup(**ndgroupdata)
            ret = ndgroup.valid_data
            self.set_status(201)
            logging.info("Create NodeGroup: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(400)
            logging.error("Create NodeGroup Error: %s" % ret)
        finally:
            self.finish(ret)

    def gets(self, ndgroupid):
        """
        HTTP 方法: GET

        客户端根据ndgroupid读取一条NodeGroup数据，若正常返回200和NodeGroup数据，若
        根据该ndgroupid未找到数据则返回404，内部错误返回500.
        """
        try:
            ret = NodeGroup.get_data_by_id(_id=ndgroupid)
            if ret is None:
                ret = {"status": 404, "message": "NodeGroup Not Found!",
                       "ndgroupid": ndgroupid}
                self.set_status(404)
                logging.warning("NodeGroup Not Found: %s" % ndgroupid)
            else:
                self.set_status(200)
                logging.info("Query NodeGroup: %s, %s" % (ndgroupid, ret))
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get NodeGroup Error: %s, %s" % (ndgroupid, ret))
        finally:
            self.finish(ret)

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明ndgroupid时，返回所有NodeGroup信息，需考虑分页
        """
        try:
            ret = NodeGroup.all_data()
            if not ret:
                ret = {"status": 404, "message": "There has no NodeGroup!"}
                self.set_status(404)
                logging.warning("NodeGroup collection Not Found.")
            else:
                ret = {
                    'draw': 1,
                    'recordsTotal': len(ret),
                    'recordsFiltered': len(ret),
                    'data': ret
                }
                self.set_status(200)
                logging.info("Query NodeGroup collection: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get NodeGroup collection Error: %s" % ret)
        finally:
            self.finish(ret)

    def update(self, ndgroupid):
        """
        HTTP 方法: PUT

        根据ndgroupid全量更新一条NodeGroup数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有NodeGroup数据, 批量更新
        """
        pass

    def delete(self, ndgroupid):
        """
        HTTP 方法: DELETE

        根据nodeid删除一条NodeGroup数据，可以物理删除或逻辑删除，删除后再被GET请求
        时应报错404。
        """
        pass

    def delete_collection(self):
        """
        HTTP 方法: DELETE

        删除所有NodeGroup数据，批量删除
        """
        pass
