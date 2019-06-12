#!/usr/bin/env python3

import re
import sys
import time
import logging
import traceback
import configparser
from datetime import datetime, timedelta
from subprocess import check_output

import psutil
from matrix_client.client import MatrixClient

class Bender():
    def __init__(self, config_path, logger):
        self.logger = logger
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.connect()
        

        self.client.start_listener_thread()

        self.sys_status()
        self.parse_auth_log()

        while self.running:
            time.sleep(1)

    def connect(self):
        host = self.config.get("bender", "host")
        user = self.config.get("bender", "user")
        password = self.config.get("bender", "password")
        display_name = self.config.get("bender", "display_name")
        room = self.config.get("bender", "room")
        try:
            self.client = MatrixClient(host)
            self.client.login(username=user, password=password)
            self.room = self.client.join_room(room)
            self.room.add_listener(self.on_room_event)
            self.running = True

            self.user = self.client.get_user(self.client.user_id)
            self.user.set_display_name(display_name)
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.error(repr(e))
            self.logger.critical(trace)

    def on_room_event(self, room, event):
        if event["sender"] == self.client.user_id:
            return
        if event["type"] != "m.room.message":
            return
        if event["content"]["msgtype"] != "m.text":
            return
        if event["content"]["body"].startswith("!status"):
            self.sys_status()
        if event["content"]["body"].startswith("!checklog"):
            self.parse_auth_log()
        # Fix this
        if event["content"]["body"].startswith("!byerobot"):
            self.room.send_text("Bite my shiny metal ass!")
            #sys.exit(0)
            #self.client.stop_listener_thread()
            #self.client.logout()
            #self.running = False

    def sys_status(self):
        ssh_status = check_output("systemctl status ssh", shell=True).decode("utf-8")
        ssh_status = ssh_status.split("\n")
        msg = [f"SSHD status: {re.search('Active: (.*)$', ssh_status[2]).group(1)}"]
        msg.append(f"Last action: {ssh_status[-2]}")
        msg.append(f"Memory utilization: {psutil.virtual_memory()[2]}%")
        msg.append(f"Storage disk utilization: {psutil.disk_usage('/media/wkg/storage')[3]}%")
        for temp in psutil.sensors_temperatures()['coretemp'][1:]:
            msg.append(f"{temp[0]}: {temp[1]} C")
        nvidia_stat = check_output("nvidia-smi", shell=True).decode("utf-8")
        nvidia_stat = nvidia_stat.split("\n")[8]
        fan = re.search('^\|\s*(\d*%)', nvidia_stat).group(1)
        msg.append(f"GPU fan: {fan}")
        temp = re.search('\d*C', nvidia_stat).group()
        msg.append(f"GPU temp: {temp}")
        power = re.search('\d*W\s/\s\d*W', nvidia_stat).group()
        msg.append(f"GPU power usage: {power}")
        memory = re.search('\d*MiB\s/\s*\d*MiB', nvidia_stat).group()
        msg.append(f"GPU memory util.: {memory}")

        msg = "\n".join(msg)
        self.room.send_text(msg)

    def parse_auth_log(self):
        today = datetime.now()
        yesterday = datetime.now() - timedelta(1)

        sshd_failed = []
        with open("/var/log/auth.log", "r") as log:
            for line in log:
                match_today = re.search(f"^{today.strftime('%b')}\s+{today.day}", line)
                match_yesterday = re.search(f"^{yesterday.strftime('%b')}\s+{yesterday.day}", line)
                if match_today or match_yesterday:
                    if re.search("sshd.*Failed", line):
                        sshd_failed.append(line)
                    if re.search("sshd.*Connection closed", line):
                        sshd_failed.append(line)

        failed_ips = []
        for fail in sshd_failed:
            match = re.search("\d+\.\d+\.\d+\.\d+", fail)
            if match:
                failed_ips.append(match.group())
        failed_ips = list(dict.fromkeys(failed_ips))

        msg = [f"{str(len(sshd_failed))} failed SSH login/authentication attempt(s) occurred in the past " \
            "two days."]

        if len(sshd_failed) > 0:
            msg.append("Failures originated from IP address(es):")
            for ip in failed_ips:
                msg.append(ip)

        msg = "\n".join(msg)

        self.room.send_text(msg)

def main():
    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("bender.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    Bender("bot.cfg", logger)

if __name__ == "__main__":
    main()