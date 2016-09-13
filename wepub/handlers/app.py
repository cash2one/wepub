#!/usr/bin/env python
# encoding: utf-8

import logging
import traceback

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

        eg:
        curl -H "Content-Type: application/json" -X POST -d '{
            "name":"container_monitor",
            "version":"0.0.7",
            "platform":"el6.x84_64",
            "packagesource":"a url to package",
            "administrator":"denglj"}' http://127.0.0.1:8000/app
        """
        try:
            appdata = json_decode(self.request.body)
            # when create an `App` object, will automaticly save data to db
            app = App(**appdata)
            ret = app.valid_data
            self.set_status(201)
            logging.info("Create App: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(400)
            logging.error("Create App Error: %s" % ret)
        finally:
            self.finish(ret)

    def gets(self, appid):
        """
        HTTP 方法: GET

        客户端根据appid读取一条App数据，若正常返回200和App数据，若
        根据该appid未找到数据则返回404，内部错误返回500.
        """
        try:
            ret = App.get_data_by_id(_id=appid)
            if ret is None:
                ret = {"status": 404, "message": "App Not Found!",
                       "appid": appid}
                self.set_status(404)
                logging.warning("App Not Found: %s" % appid)
            else:
                self.set_status(200)
                logging.info("Query App: %s, %s" % (appid, ret))
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get App Error: %s, %s" % (appid, ret))
        finally:
            self.finish(ret)

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明appid时，返回所有App信息，需考虑分页
        """
        try:
            ret = App.all_data()
            if not ret:
                ret = {"status": 404, "message": "There has no App!"}
                self.set_status(404)
                logging.warning("App collection Not Found.")
            else:
                self.set_status(200)
                logging.info("Query App collection: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get App collection Error: %s" % ret)
        finally:
            self.finish(ret)

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
