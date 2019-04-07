#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 18:59:38 2019

@author: wigasper
"""

#https://www.devdungeon.com/content/make-discord-bot-python

# Work with Python 3.6
import discord

TOKEN = 'NTY0MjM2NDU1ODEyMjY4MDMy.XKk8Ug.-gz3XEcICHYdxyU5yhFNgrX-YFE'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)