#!/usr/bin/env python3

import sys
import argparse

import discord

def notify(msg):
    if msg is None:
        msg = "Job complete"
    
    # creds format:
    # [TOKEN, SERVER, CHANNEL]
    creds = []

    # credentials.txt should consist of the following elements
    # in the following format
    # token\nserver\nchannel
    # token, server, and channel in that order separated by newlines
    with open("/media/wkg/storage/bender/credentials.txt") as fp:
        for line in fp:
            creds.append(line.strip("\n"))
    
    TOKEN = creds[0]

    SERVER = creds[1]

    CHANNEL = creds[2]

    client = discord.Client()

    @client.event
    async def on_ready(): 
        server = client.get_server(SERVER)
        await client.send_message(server.get_channel(CHANNEL), msg)
        await client.logout()

    client.run(TOKEN)

def main():
    # Get command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="a message to have the bot send")
    args = parser.parse_args()

    if args.message:
        msg = args.message
    else:
        msg = sys.stdin.read()

    notify(msg)

if __name__ == '__main__':
    main()