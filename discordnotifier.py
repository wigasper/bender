#!/usr/bin/env python3

import sys
import getopt

import discord

def discord_notification(msg):
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

def usage():
    print("\nUsage: ", sys.argv[0], " \n")

class discordnotifier:
    
    def main():
        options = {}        # Command line options dict
        
        # Read in the command-line arguments into the opts
        try:
            opts, args = getopt.getopt(sys.argv[1:], "m:")
        
        except getopt.GetoptError as err:
            sys.stdout = sys.stderr

            # Print help information
            print(str(err))

            usage()

            # Exit the program
            sys.exit(2)
            
        for (opt, arg) in opts:
            options[opt] = arg
            
        if "-m" in options.keys():
            msg = options["-m"]
        else:
            msg = sys.stdin.read()

        discord_notification(msg)

    if __name__ == '__main__':
        main()