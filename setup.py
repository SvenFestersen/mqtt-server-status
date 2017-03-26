#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from culmqtt import __version__ as ver


setup(name="status-mqtt",
      version=ver,
      description="Server status monitor.",
      author="Sven Festersen",
      author_email="sven@sven-festersen.de",
      packages=["mqttstatus"],
      requires=["paho.mqtt"],
      scripts=["cli/status-mqtt"]
     )
