#!/usr/bin/env python

import os
import glob
import subprocess
import json
import psutil
from os.path import splitext, basename, realpath

CEPH_SOCKET_PATH = os.getenv("CEPH_RUN_PATH", "/var/run/ceph/")

class CephSrvInfo(object):
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid


def get_ceph_pids():
    """Return PIDs as list of SrvInfo for all CEPH
    services on local node.
    """
    pids = []
    for srv in get_srv_list():
        cfg = get_srv_config(srv)
        with open(cfg['pid_file'], 'r') as file_fd:
            pids.append(CephSrvInfo(srv, int(file_fd.read())))

    return pids

def get_ceph_disk():
    """Return list of disk devices wich is used by all
       CEPH services on local node."""
    disks = []
    for srv in get_srv_list():
        cfg = get_srv_config(srv)
        for key in ['osd_data', 'osd_journal', 'mds_data', 'mon_data']:
            mnt_point = cfg[key]
            disk = get_disk_by_mountpoint(find_mount_point(mnt_point))
            if disk not in disks:
                disks.append(disk)
    return disks

def get_srv_list():
    """ Returns list of srv (ceph creatures) on node """
    srv_list = [splitext(basename(sock))[0] \
                for sock in glob.glob(CEPH_SOCKET_PATH + "*.asok")]
    return srv_list

def get_srv_config(name):
    """ Get CEPH Service Config """
    cmd = "ceph --admin-daemon %s/%s.asok config show" % \
        (CEPH_SOCKET_PATH, name)
    out = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return json.loads(out.stdout.read())

def get_disk_by_mountpoint(mnt_point):
    """ Return disk of mountpoint """
    diskparts = psutil.disk_partitions()
    for item in diskparts:
        if item.mountpoint == mnt_point:
            return realpath(item.device)
    return None

def find_mount_point(path):
    """ Find mount point by provided path """
    path = os.path.abspath(path)
    while not os.path.ismount(path):
        path = os.path.dirname(path)
    return path

def test():
    for srv in get_ceph_pids():
        print 'Service %s has pid %d' % (srv.name, srv.pid)
    print get_ceph_disk()

if __name__ == '__main__':
    test()
