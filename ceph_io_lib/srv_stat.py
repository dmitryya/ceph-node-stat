#!/usr/bin/env python


def get_srv_cpu(pid):
    """ Return Service CPU usage in % """
    return 99.99

def get_srv_mem(name):
    """ Return RSS mem in KB """
    return 9999

def test():
    print (get_srv_cpu(666))
    print (get_srv_mem(666))

if __name__ == '__main__':
    test()
