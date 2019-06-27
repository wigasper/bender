# bender
Bender is my friendly Matrix bot that does a few simple tasks. He provides simple system status updates and parses my auth log for SSH events. The bot.py file can be run persistently as a systemd service (ideally) or started as a cron job.

A particularly useful feature is the notify.py script:

**notify.py** - This script can be used to send a notification on demand. I use it to send me notifications when long jobs have been completed and when SSH logins occur. It can be used:
* By Python: if copied to your lib/python3.6 directory it can easily be used with an import and a single call
```python
from notify import notify
notify("Oh hello")
```
* At the command line, in Bash scripts, or with system calls in other languages: by using the -m option followed by the desired message
```
python3 notify.py -m "Oh hello"
```
* At the command line, in Bash scripts, or with system calls in other languages: by piping the desired message into stdin
```
echo "Oh hello" | python3 notify.py
```
sshd-login is an example of a simple script that can send a message with every SSH login. To make this happen, a line like this can be added to /etc/pam.d/sshd:
```
session    optional     pam_exec.so /path/to/sshd-login
```
