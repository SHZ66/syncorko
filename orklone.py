#!/usr/bin/env python3
import configparser
from sys import argv
from os.path import join
from os.path import abspath

def run_cmd(cmd):
    from subprocess import Popen, PIPE
    from shlex import split as shplit
    process = Popen(shplit(cmd), stdout=PIPE)
    output, error = process.communicate()
    return output, error

try:
    load = argv[1].lower()
    folder = argv[2]
    args = argv[3:]
except:
    raise ValueError('at least 2 arguments are expected')



config = configparser.ConfigParser()
config.read('settings.cfg')

local_folder = config['PATHS']['LocalFolder']
remote_folder = config['PATHS']['RemoteFolder']

if 'up' in load:
    src = join(local_folder, folder)
    des = join(remote_folder, folder)
elif 'down' in load:
    src = join(remote_folder, folder)
    des = join(local_folder, folder)
else:
    raise ValueError('wrong command: %s'%load)

if 'sync' in load:
    type_ = 'sync'
elif 'copy' in load:
    type_ = 'copy'

cmd = 'rclone {type} "{src}" "{des}" '.format(type=type_, src=src, des=des)

strargs = ' '.join(args)
cmd += strargs

print(cmd)

output, err = run_cmd(cmd)
if output is not None:
    print(output.decode())
if err is not None:
    print(err)

# ln -s /home/shz66/syncorko/orklone.sh /home/shz66/bin/orklone
