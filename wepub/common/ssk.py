#!/usr/bin/env python
# encoding: utf-8


import logging
import salt.client
import salt.config
import salt.loader


class Salt(object):

    def __init__(self, master):
        self.master = master

    def cmd(self, target, func, args, **kwargs):
        logging.info("SaltStack Command: target:{0}, function:{1}, args:{2}, kwargs:{3}".format(
            *map(str, [target, func, args, kwargs])))
        return self.master.cmd(target, func, args, **kwargs)

    def cmd_async(self, target, func, args, **kwargs):
        logging.info("SaltStack Command: target:{0}, function:{1}, args:{2}, kwargs:{3}".format(
            *map(str, [target, func, args, kwargs])))
        return self.master.cmd_async(target, func, args, **kwargs)

    def run_job(self, target, func, args, **kwargs):
        logging.info("SaltStack Command: target:{0}, function:{1}, args:{2}, kwargs:{3}".format(
            *map(str, [target, func, args, kwargs])))
        return self.master.run_job(target, func, args, **kwargs)

if __name__ == '__main__':
    ssk = Salt(salt.client.LocalClient())
    res = ssk.master.cmd('*', 'cmd.run', ['whoami'])
    res2 = ssk.cmd('*', 'test.arg', ['arg1', 'arg2'], kwarg={'foo': 'bar'})
    print res
    print res2
