#!/usr/bin/env python3

import sys
import argparse
import configparser
import socket

def notify(msg):
    if msg is None:
        msg = "Job complete"
    
    config = configparser.ConfigParser()
    config.read("/media/wkg/storage/bender/bot.cfg")
    
    LOCAL_HOST = config.get("bender", "local_host")
    PORT = int(config.get("bender", "port"))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOCAL_HOST, PORT))
        s.sendall(str.encode(msg))

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
