#!/usr/bin/env python

import os
import glob
import subprocess
import json
import psutil
from os.path import splitext, basename, realpath

CEPH_SOCKET_PATH = os.getenv("CEPH_RUN_PATH", "/var/run/ceph/")

class CEPHSrvInfo(object):
    def __init__(self, name, pid, cpu=0, mem=0):
        self.name = name
        self.pid = pid
        self.cpu = cpu
        self.mem = mem

class CEPHDiskInfo(object):
    def __init__(self, name, rd_cnt=0, wr_cnt=0, rd_bytes=0,
                    wr_bytes=0, rd_time=0, wr_time=0):
        self.name = name
        self.rd_cnt = rd_cnt
        self.wr_cnt = wr_cnt
        self.rd_bytes = rd_bytes
        self.wr_bytes = wr_bytes
        self.rd_time = rd_time
        self.wr_time = wr_time

def get_ceph_srv_info():
    """ Return list of CEPHSrvInfo for all CEPH services on the local node """
    services = []
    for name, pid in get_ceph_pids():
        process = psutil.Process(pid)
        services.append(CEPHSrvInfo(name, pid, process.get_cpu_percent(),\
                                        process.memory_info().rss))
    return services

def get_ceph_drv_info():
    """ Return list of CEPHDiskInfo for all disks that used by CEPH on the
        local node 
    """
    disks_info = []
    stat = psutil.disk_io_counters(perdisk=True)
    for drv in get_ceph_disk():
        info = CEPHDiskInfo(drv)
        disk = basename(drv)
        if disk in stat:
            info.rd_cnt = stat[disk].read_count
            info.wr_cnt = stat[disk].write_count
            info.rd_bytes = stat[disk].read_bytes
            info.wr_bytes = stat[disk].write_bytes
            info.rd_time = stat[disk].read_time
            info.wr_time = stat[disk].write_time

        disks_info.append(info)

    return disks_info
        

def get_ceph_pids():
    """ Return list tuple (NAME, PID) as list of SrvInfo for all CEPH
        services on local node.
    """
    pids = []
    for srv in get_srv_list():
        cfg = get_srv_config(srv)
        with open(cfg['pid_file'], 'r') as file_fd:
            pids.append((srv, int(file_fd.read())))
    return pids

def get_ceph_disk():
    """ Return list of disk devices wich is used by all
        CEPH services on local node.
    """
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
    for srv in get_ceph_srv_info():
        print 'Service %s: pid %d, cpu %d%%, mem %d bytes' % \
            (srv.name, srv.pid, srv.cpu, srv.mem)

    for disk in get_ceph_drv_info():
        print ('DISK %s: read count %d, write count %d, read bytes %d,'
              'write bytes %d, read time %d, write time %d') % \
            (disk.name, disk.rd_cnt, disk.wr_cnt, disk.rd_bytes, disk.wr_bytes, \
            disk.rd_time, disk.wr_time)

if __name__ == '__main__':
    test()
