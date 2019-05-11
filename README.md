# bender
Bender is my friendly Discord bot that does a handful of simple tasks. I update him as needed. He provides simple system status updates and parses SSH logs. A particularly useful feature is the discordnotifier.py script:

**discordnotifier.py** - This script can be used to send a notification on demand. I use it to send me notifications when long jobs have been completed and when SSH logins occur. It can be used:
* In Python scripts, by putting it in /lib/python3.6 it can easily be used with an import statement and a single call
* At the command line or in Bash scripts, by using the -m option followed by the desired message, or without the -m message and an ambiguous message will be sent
* At the command line or in Bash scripts, by piping the desired message into stdin

sshd-login is an example of a simple script that can will send a message with every SSH login. To make this happen, a line like this can be added to /etc/pam.d/sshd:
    session    optional     pam_exec.so /path/to/sshd-login
