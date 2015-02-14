#!/usr/bin/env python

import os
import glob
import subprocess
from os.path import splitext, basename

class CEPHLocalSrvInfo():
    def __init__(self, adm_socket_path='/var/run/ceph'):
        self.adm_socket_path=adm_socket_path

    def get_pids(self):
            """Return PIDs as list of dict (name, pid) for all CEPH
            services on local node.
            """
            return [{'name':'osd.0', 'pid':1000}, {'name':'mon.0', 'pid':1001}, {'name':'mds.0', 'pid':1002}]

    def get_disk(self):
            """Return list of disk devices wich is used by all CEPH services on local node."""
            return ['/dev/sdx', '/dev/sdy', '/dev/sdz']

    def _get_srv_list(self):
            """ Returns list of srv (ceph creatures) on node """
            srv_list = [splitext(basename(sock))[0] for sock in glob.glob(self.adm_socket_path + "*.asok")]
            return srv_list
    
    def _get_srv_config(self, name):
            """ Get CEPH Service Config """
            cmd = "ceph --admin-daemon %s/%s.asok perf %s" % (self.adm_socket_path, name)
            PIPE = subprocess.PIPE
            p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
            return json.loads(p.stdout.read())


def test():
    node = CEPHLocalSrvInfo()
    for srv in node.get_pids():
        print 'Service %s has pid %d' % (srv['name'], srv['pid'])
    print (node.get_disk())

if __name__ == '__main__':
    test()
