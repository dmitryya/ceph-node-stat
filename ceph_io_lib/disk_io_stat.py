#!/usr/bin/env python


def get_disk_bandwidth(name):
    """ Return disk bandwidth in KB/s (read, write)"""
    return (1000.99, 99.1000)

def get_disk_iops(name):
    """ Return disk IOPS for all time (read, write) """
    return (99, 66)

def get_disk_latency(name):
    """ Return disk latency in ms (read, write)"""
    return (13, 31)

def test():
    print (get_disk_bandwidth('/dev/sdx'))
    print (get_disk_iops('/dev/sdx'))
    print (get_disk_latency('/dev/sdx'))

if __name__ == '__main__':
    test()
