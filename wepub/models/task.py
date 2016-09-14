#!/usr/bin/env python
# encoding: utf-8


from tornado.escape import json_decode

from .base import Model
from .base import String, RegexString

import salt.client
from wepub.common.ssk import Salt


class Job(Model):
    name = String()
    status = RegexString(pat=r'(\bwaiting\b)|(\bexecuting\b) \
                             |(\bstopped\b)|(\bcompleted\b) \
                             |(\bsuspend\b)')
    cmdtype = String()
    cmd = String()

    @property
    def valid_data(self):
        data = {}
        _ = vars(self)
        for key, val in _.items():
            # valid every field here
            data[key] = val
        return data


class Task(Model):
    name = String()
    appid = String()
    nodes = String()
    nodes_success = String()
    nodes_failed = String()
    jobs = String()
    status = RegexString(pat=r'(\bwaiting\b)|(\bexecuting\b) \
                             |(\bstopped\b)|(\bcompleted\b) \
                             |(\bsuspend\b)')
    creator = String()
    starttime = String()
    endtime = String()

    @property
    def valid_data(self):
        data = {}
        _ = vars(self)
        for key, val in _.items():
            # valid every field here
            data[key] = val
        return data

    @classmethod
    def execute(cls, taskid):
        # TODO: 这里执行任务的方式改成异步的，可以一次发出多个请求不必阻塞等待每一个完成
        taskfields = sorted(['_id', 'timestamp', 'name', 'appid', 'nodes',
                       'nodes_success', 'nodes_failed', 'jobs',
                       'status', 'creator', 'starttime', 'endtime'])
        taskdct = dict(zip(taskfields, cls.get_data_by_id(taskid)))
        jobfields = sorted(['_id', 'timestamp', 'cmdtype', 'cmd', 'status', 'name'])
        jobids = taskdct['jobs'].split(',')
        jobs = []
        for jobid in jobids:
            jobdct = dict(zip(jobfields, Job.get_data_by_id(jobid)))
            jobs.append((jobid, jobdct))
        ss = Salt(salt.client.LocalClient())
        ret = {}
        for jobid, jobdct in jobs:
            _ret = ss.cmd(taskdct['nodes'], jobdct['cmdtype'], [jobdct['cmd']])
            ret[jobid] = _ret
        return ret
