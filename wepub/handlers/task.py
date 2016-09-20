#!/usr/bin/env python
# encoding: utf-8

import logging
import traceback

from tornado.escape import json_decode

from wepub.common import RESTfulHandler
from wepub.models.task import Task, Job


class TaskHandler(RESTfulHandler):
    """
    处理客户端对Task资源发出的HTTP请求
    """

    def create(self):
        """
        HTTP 方法: POST

        在数据库中新增一条Task数据，若创建Task成功则返回状态码201，
        创建失败则返回400，遇到内部错误返回500.

        eg:
        curl -H "Content-Type: application/json" -X POST -d '{
            "name":"install_monitor",
            "status":"waiting",
            "cmdtype":"cmd.run",
            "cmd":"yum install -y container-monitor-agent"
            }' http://127.0.0.1:8000/task
        """
        try:
            taskdata = json_decode(self.request.body)
            # when create an `Task` object, will automaticly save data to db
            task = Task(**taskdata)
            ret = task.valid_data
            self.set_status(201)
            logging.info("Create Task: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(400)
            logging.error("Create Task Error: %s" % ret)
        finally:
            self.finish(ret)

    def start(self, taskid):
        """
        HTTP 方法：POST

        根据taskid启动任务
        """
        try:
            ret = Task.execute(taskid)
            if ret is None:
                ret = {"status": 404, "message": "Task Start Failed!",
                       "taskid": taskid}
                self.set_status(404)
                logging.warning("Task Start Failed: %s" % taskid)
            else:
                self.set_status(200)
                logging.info("Task Executed: %s, %s" % (taskid, ret))
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Task Start Error: %s, %s" % (taskid, ret))
        finally:
            self.finish(ret)

    def gets(self, taskid):
        """
        HTTP 方法: GET

        客户端根据taskid读取一条Task数据，若正常返回200和Task数据，若
        根据该taskid未找到数据则返回404，内部错误返回500.
        """
        try:
            ret = Task.get_data_by_id(_id=taskid)
            if ret is None:
                ret = {"status": 404, "message": "Task Not Found!",
                       "taskid": taskid}
                self.set_status(404)
                logging.warning("Task Not Found: %s" % taskid)
            else:
                self.set_status(200)
                logging.info("Query Task: %s, %s" % (taskid, ret))
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get Task Error: %s, %s" % (taskid, ret))
        finally:
            self.finish(ret)

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明taskid时，返回所有Task信息，需考虑分页
        """
        try:
            ret = Task.all_data()
            if not ret:
                ret = {"status": 404, "message": "There has no Task!"}
                self.set_status(404)
                logging.warning("Task collection Not Found.")
            else:
                self.set_status(200)
                logging.info("Query Task collection: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get Task collection Error: %s" % ret)
        finally:
            self.finish(ret)

    def update(self, taskid):
        """
        HTTP 方法: PUT

        根据taskid全量更新一条Task数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有Task数据, 批量更新
        """
        pass

    def delete(self, taskid):
        """
        HTTP 方法: DELETE

        根据taskid删除一条Task数据，可以物理删除或逻辑删除，删除后再被GET请求
        时应报错404。
        """
        pass

    def delete_collection(self):
        """
        HTTP 方法: DELETE

        删除所有Task数据，批量删除
        """
        pass


class JobHandler(RESTfulHandler):
    """
    处理客户端对Job资源发出的HTTP请求
    """

    def create(self):
        """
        HTTP 方法: POST

        在数据库中新增一条Job数据，若创建Job成功则返回状态码201，
        创建失败则返回400，遇到内部错误返回500.

        eg:
        curl -H "Content-Type: application/json" -X POST -d '{
            "name":"install_monitor",
            "status":"waiting",
            "cmdtype":"cmd.run",
            "cmd":"yum install -y container-monitor-agent"
            }' http://127.0.0.1:8000/job
        """
        try:
            jobdata = json_decode(self.request.body)
            # when create an `Job` object, will automaticly save data to db
            job = Job(**jobdata)
            ret = job.valid_data
            self.set_status(201)
            logging.info("Create Job: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(400)
            logging.error("Create Job Error: %s" % ret)
        finally:
            self.finish(ret)

    def gets(self, jobid):
        """
        HTTP 方法: GET

        客户端根据jobid读取一条Job数据，若正常返回200和Job数据，若
        根据该jobid未找到数据则返回404，内部错误返回500.
        """
        try:
            ret = Job.get_data_by_id(_id=jobid)
            if ret is None:
                ret = {"status": 404, "message": "Job Not Found!",
                       "jobid": jobid}
                self.set_status(404)
                logging.warning("Job Not Found: %s" % jobid)
            else:
                self.set_status(200)
                logging.info("Query Job: %s, %s" % (jobid, ret))
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get Job Error: %s, %s" % (jobid, ret))
        finally:
            self.finish(ret)

    def lists(self):
        """
        HTTP 方法: GET

        请求未指明jobid时，返回所有Job信息，需考虑分页
        """
        try:
            ret = Job.all_data()
            if not ret:
                ret = {"status": 404, "message": "There has no Job!"}
                self.set_status(404)
                logging.warning("Job collection Not Found.")
            else:
                self.set_status(200)
                logging.info("Query Job collection: %s" % ret)
        except:
            ret = traceback.format_exc()
            self.set_status(500)
            logging.error("Get Job collection Error: %s" % ret)
        finally:
            self.finish(ret)

    def update(self, jobid):
        """
        HTTP 方法: PUT

        根据jobid全量更新一条Job数据，需传递更新后的全量数据，而非改变量
        """
        pass

    def update_collection(self):
        """
        HTTP 方法: PUT

        更新所有Job数据, 批量更新
        """
        pass

    def delete(self, jobid):
        """
        HTTP 方法: DELETE

        根据jobid删除一条Job数据，可以物理删除或逻辑删除，删除后再被GET请求
        时应报错404。
        """
        pass

    def delete_collection(self):
        """
        HTTP 方法: DELETE

        删除所有Job数据，批量删除
        """
        pass
