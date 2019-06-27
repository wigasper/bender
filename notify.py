#!/usr/bin/env python3

import sys
import argparse
import configparser

from matrix_client.client import MatrixClient

def notify(msg):
    if msg is None:
        msg = "Job complete"
    
    config = configparser.ConfigParser()
    config.read("/media/wkg/storage/bender/bot.cfg")

    host = config.get("bender", "host")
    user = config.get("bender", "user")
    password = config.get("bender", "password")
    room = config.get("bender", "room")

    client = MatrixClient(host)
    client.login(username=user, password=password)
    room = client.join_room(room)
    room.send_text(msg)

    client.logout()

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