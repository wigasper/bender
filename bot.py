#!/usr/bin/env python3

import re
from datetime import datetime, timedelta
import asyncio
import time
from subprocess import Popen, PIPE

import discord
import psutil

# creds format:
# [TOKEN, SERVER, CHANNEL]
creds = []

# credentials.txt should consist of the following elements
# in the following format
# token\nserver\nchannel
# token, server, and channel in that order separated by newlines
with open("credentials.txt") as fp:
    for line in fp:
        creds.append(line.strip("\n"))

TOKEN = creds[0]

SERVER = creds[1]

CHANNEL = creds[2]

client = discord.Client()

@client.event
async def on_message(message):
    # prevent bot from replying to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!sysstatus'):
        await sys_status()

    if message.content.startswith('!checklog'):
        await parse_ssh_log()

    if message.content.startswith('!byerobot'):
        msg = 'Bite my shiny metal ass!'
        await client.send_message(message.channel, msg)
        await client.logout()

async def sys_status():
    server = client.get_server(SERVER)
    with Popen("systemctl status ssh", stdout=PIPE, stderr=PIPE, shell=True) as proc:
        ssh_status = proc.communicate()[0].decode("utf-8")
    ssh_status = ssh_status.split("\n")
    msg = f"**SSHD status:** {re.search('Active: (.*)$', ssh_status[2]).group(1)}"
    await client.send_message(server.get_channel(CHANNEL), msg)
    msg = f"**Last action:** {ssh_status[-2]}"
    await client.send_message(server.get_channel(CHANNEL), msg)
    msg = f"**Memory utilization:** {psutil.virtual_memory()[2]}%"
    await client.send_message(server.get_channel(CHANNEL), msg)
    msg = f"**Storage disk utilization:** {psutil.disk_usage('/media/wkg/storage')[3]}%"
    await client.send_message(server.get_channel(CHANNEL), msg)
    for temp in psutil.sensors_temperatures()['coretemp'][1:]:
        msg = f"**{temp[0]}:** {temp[1]} C"
        await client.send_message(server.get_channel(CHANNEL), msg)
    with Popen("nvidia-smi", stdout=PIPE, stderr=PIPE, shell=True) as proc:
        nvidia_stat = proc.communicate()[0].decode("utf-8")
        if nvidia_stat:
            nvidia_stat = nvidia_stat.split("\n")[8]
            fan = re.search('^\|\s*(\d*%)', nvidia_stat).group(1)
            msg = f"**GPU fan:** {fan}"
            await client.send_message(server.get_channel(CHANNEL), msg)
            temp = re.search('\d*C', nvidia_stat).group()
            msg = f"**GPU temp:** {temp}"
            await client.send_message(server.get_channel(CHANNEL), msg)
            power = re.search('\d*W\s/\s\d*W', nvidia_stat).group()
            msg = f"**GPU power usage:** {power}"
            await client.send_message(server.get_channel(CHANNEL), msg)
            memory = re.search('\d*MiB\s/\s*\d*MiB', nvidia_stat).group()
            msg = f"**GPU memory util.:** {memory}"
            await client.send_message(server.get_channel(CHANNEL), msg)

async def parse_ssh_log():
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

    msg = f"**{str(len(sshd_failed))}** failed SSH login/authentication attempt(s) occurred in the past " \
          "two days."

    server = client.get_server(SERVER)
    await client.send_message(server.get_channel(CHANNEL), msg)
    if len(sshd_failed) > 0:
        msg = "**Failures originated from IP address(es):**"
        await client.send_message(server.get_channel(CHANNEL), msg)
        for ip in failed_ips:
            await client.send_message(server.get_channel(CHANNEL), ip)

async def send_interval_message():
    await client.wait_until_ready()
    interval = 86400
    while not client.is_closed:
        await sys_status()
        await parse_ssh_log()
        await asyncio.sleep(interval)

@client.event
async def on_ready():
    client.loop.create_task(send_interval_message())

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)

