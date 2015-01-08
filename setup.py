#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='Talking Sockets',
      version='1.0',
      description='Connection routing library',
      author='Dana Christen',
      author_email='dana.christen@gmail.com',
      url='https://github.com/danac/talking-sockets',
      packages=['talking_sockets'],
      install_requires=['autobahn', 'asyncio'],
      license='AGPLv3+',
      zip_safe=True,
      keywords='websocket tcp router connection relay asyncio autobahn',
      classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.4",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Networking",
            ],
     )
