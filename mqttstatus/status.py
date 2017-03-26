# -*- coding: utf-8 -*-
from .utils import *
import paho.mqtt.client as paho
import logging
import time


def make_messages(info, parent=""):
    messages = []
    for k in info:
        v = info[k]
        if type(v) == dict:
            messages += make_messages(v, parent + k + "/")
        else:
            messages.append((parent + k, v))
    return messages


class ServerStatus(object):
    
    def __init__(self, broker, name, update_interval, platform=False,
                 uptime=False, memory=False, load=False, storage=[],
                 log_level=logging.ERROR):
        super(ServerStatus, self).__init__()
        self._broker = broker
        self._name = name
        self._update_interval = update_interval
        self._platform = platform
        self._uptime = uptime
        self._memory = memory
        self._load = load
        self._storage = storage
        self._log_level = log_level
        self._run = True

    def start(self):
        self._client = paho.Client(client_id=self._name)
        self._client.connect(self._broker, 1883)
        self._client.loop_start()
        while self._run:
            self.publish_info()
            time.sleep(self._update_interval)
        
    def stop(self):
        self._run = False
        self._client.loop_stop()
        
    def publish_info(self):
        messages = []
        if self._platform:
            info = get_platform()
            messages += make_messages(info, "server/platform/")
        if self._uptime:
            info = get_uptime()
            messages += make_messages(info, "server/uptime/")
        if self._memory:
            info = get_memory()
            messages += make_messages(info, "server/memory/")
        if self._load:
            info = get_load()
            messages += make_messages(info, "server/load/")
        if self._storage:
            info = get_storage(self._storage)
            messages += make_messages(info, "server/storage/")
        for d in messages:
            topic, value = d
            self._client.publish(topic + "/" + self._name, value)
