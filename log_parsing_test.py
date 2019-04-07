#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

today = datetime.now()
yesterday = datetime.now() - timedelta(1)

sshd_failed = []
sshd_did = []

# probably should make this sys.stdin to take tail

#with open("/var/log/auth.log", "r") as log:
with open("auth.log", "r") as log:
    for line in log:
        match_today = re.search("^{}  {}".format(today.strftime("%b"), 
                            today.day), line)
        match_yesterday = re.search("^{}  {}".format(yesterday.strftime("%b"), 
                            yesterday.day), line)
        if match_today or match_yesterday:
            if re.search("sshd.*Failed", line):
                sshd_failed.append(line)
            if re.search("sshd.*Did", line):
                sshd_failed.append(line)

failed_ips = []

msg = "There has been {} failed login attempts in the " \
      "past two days.".format(str(len(sshd_failed)))