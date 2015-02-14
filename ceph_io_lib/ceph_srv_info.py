#!/usr/bin/env python

import os
import glob
import subprocess
import json
from os.path import splitext, basename

CEPH_SOCKET_PATH = os.getenv("CEPH_RUN_PATH", "/var/run/ceph/")

def get_ceph_pids():
    """Return PIDs as list of dict (name, pid) for all CEPH
    services on local node.
    """

    pids = []

    for srv in get_srv_list():
        cfg = get_srv_config(srv)
        pid_file = cfg['pid_file']
        pid = 0
        with open(cfg['pid_file'], 'r') as f:
            pids.append({'name': srv, 'pid': int(f.read())})

    return pids

def get_ceph_disk():
    """Return list of disk devices wich is used by all CEPH services on local node."""
    return ['/dev/sdx', '/dev/sdy', '/dev/sdz']

def get_srv_list():
    """ Returns list of srv (ceph creatures) on node """
    srv_list = [splitext(basename(sock))[0] for sock in glob.glob(CEPH_SOCKET_PATH + "*.asok")]
    return srv_list

def get_srv_config(name):
    """ Get CEPH Service Config """
    cmd = "ceph --admin-daemon %s/%s.asok config show" % (CEPH_SOCKET_PATH, name)
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
    #d = p.stdout.read()
    return json.loads(p.stdout.read())


def test():
    for srv in get_ceph_pids():
        print 'Service %s has pid %d' % (srv['name'], srv['pid'])
    print (get_ceph_disk())

if __name__ == '__main__':
    test()
