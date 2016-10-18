#!/usr/bin/env python
# encoding: utf-8

import tornado.httpclient
from tornado.escape import json_decode

from oauth import get_client_id_and_secret


def get_physical_clusters():
    request_header = get_client_id_and_secret()
    url = 'http://10.176.30.209:18082/api/hcluster?type=RDS'
    request = tornado.httpclient.HTTPRequest(url, method='GET', headers=request_header)
    response = tornado.httpclient.HTTPClient().fetch(request)
    return json_decode(response.body)


def _get_containers_by_hcluster_name(name, ty):
    physical_cluster_lst = get_physical_clusters()
    for hcluster in physical_cluster_lst:
        if hcluster['hclusterName'] == name:
            hcluster_id = str(hcluster['id'])
            url = 'http://10.176.30.209:18082/db/containers/{0}?hclusterId={1}'.format(ty, hcluster_id)
            request_header = get_client_id_and_secret()
            request = tornado.httpclient.HTTPRequest(url, method='GET', headers=request_header)
            response = tornado.httpclient.HTTPClient().fetch(request)
            return json_decode(response.body)


def get_vip_containers(hcluster_name):
    containers = _get_containers_by_hcluster_name(hcluster_name, 'vip')
    containers_lst = [d['containerName'] for d in containers]
    return containers_lst


def get_db_containers(hcluster_name):
    containers = _get_containers_by_hcluster_name(hcluster_name, 'data')
    containers_lst = [d['containerName'] for d in containers]
    return containers_lst


if __name__ == '__main__':
    import pprint
    #  pprint.pprint(get_physical_clusters())
    ret = get_db_containers('MJQ_01_Mcluster')
    print(ret)
    pprint.pprint(len(ret))
