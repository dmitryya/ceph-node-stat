#!/usr/bin/env python


def get_disk_bandwidth(name):
    """ Return disk bandwidth in KB/s """
    return 1000.99

def get_disk_iops(name):
    """ Return disk IOPS """
    return 99

def get_disk_latency(name):
    """ Return disk latency in ms """
    return 13

def test():
    print (get_disk_bandwidth('/dev/sdx'))
    print (get_disk_iops('/dev/sdx'))
    print (get_disk_latency('/dev/sdx'))

if __name__ == '__main__':
    test()
