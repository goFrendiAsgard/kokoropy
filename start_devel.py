#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, signal

PWD = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(PWD,'start.py')
p = subprocess.Popen(SCRIPT_PATH)

import time
time.sleep(10)
os.kill(p.pid, signal.SIGINT)