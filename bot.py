#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#https://www.devdungeon.com/content/make-discord-bot-python
import re
from datetime import datetime, timedelta
import asyncio

import discord


TOKEN = "NTY0MjM2NDU1ODEyMjY4MDMy.XKk8Ug.-gz3XEcICHYdxyU5yhFNgrX-YFE"

SERVER = "564237008814211082"

CHANNEL = "564237008814211084"

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith('!byerobot'):
        msg = 'Bite my shiny metal ass!'
        await client.send_message(message.channel, msg)
        await client.logout()
        
async def send_interval_message():
    await client.wait_until_ready()
    interval = 86400
    while not client.is_closed:
        today = datetime.now()
        yesterday = datetime.now() - timedelta(1)
    
        sshd_failed = []
        #sshd_did = []
        with open("/var/log/auth.log", "r") as log:
        #with open("/Users/wigasper/Documents/bender/auth.log", "r") as log:
            for line in log:
                match_today = re.search("^{}  {}".format(today.strftime("%b"), 
                                    today.day), line)
                match_yesterday = re.search("^{}  {}".format(yesterday.strftime("%b"), 
                                    yesterday.day), line)
                if match_today or match_yesterday:
                    if re.search("sshd.*Failed", line):
                        sshd_failed.append(line)
                    #if re.search("sshd.*Did", line):
                    #    sshd_failed.append(line)

        failed_ips = []
        for fail in sshd_failed:
            match = re.search("\d*\.\d*\.\d*\.\d*", fail)
            if match:
                failed_ips.append(match.group())
        failed_ips = list(dict.fromkeys(failed_ips))
        
        msg = "{} failed SSH login attempt(s) occurred in the past " \
              "two days.".format(str(len(sshd_failed)))
              
        server = client.get_server(SERVER)
        await client.send_message(server.get_channel(CHANNEL), msg)
        msg = "Failures originated from IP address(es):"
        await client.send_message(server.get_channel(CHANNEL), msg)
        for ip in failed_ips:
            await client.send_message(server.get_channel(CHANNEL), ip)
            
        await asyncio.sleep(interval)

@client.event
async def on_ready():    
    client.loop.create_task(send_interval_message())
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)