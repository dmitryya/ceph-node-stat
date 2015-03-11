#!/usr/bin/env python

from distutils.core import setup

setup(name='ceph_io_lib',
      version='0.1',
      description='Gets processes and disks start for CEPH services on local node',
      author='Dzmitry Yatsushkevich',
      author_email='dyatsushkevich@mirantis.com',
      url='https://github.com/dmitryya/ceph_io_lib',
      packages=['ceph_io_lib'],
      license='LGPL',
      platforms=['linux'])
