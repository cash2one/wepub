#!/usr/bin/env python
# encoding: utf-8

from tornado import gen
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
    @gen.coroutine
    def execute(cls, taskid):
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
        # 每次并行执行N个节点的任务
        N = 30
        nodes = taskdct['nodes'].split(',')
        nodes = [nodes[x:x+N] for x in xrange(0, len(nodes), N)]

        ret = {}
        for idx, subnodes in enumerate(nodes):
            for jobid, jobdct in jobs:
                ret[str(idx)+'_'+jobid] = yield ss.cmd(subnodes,
                                                           jobdct['cmdtype'],
                                                           [jobdct['cmd']],
                                                           expr_form='list')
        raise gen.Return(ret)
