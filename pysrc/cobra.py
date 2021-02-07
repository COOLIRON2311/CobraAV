#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from os import chmod, remove, rename, scandir, stat, system
from os.path import abspath, basename, getctime, isfile, getsize
from os.path import join as path_join
from pwd import getpwuid
from stat import filemode
from sys import argv
from config import QUARANTINE_PATH
from libavctl import DataBase, enqueue_scan
from libconfig import main as config_main


class InvalidArgument(Exception):
    ...

CONTROL = 'systemctl {} cobra-sentinel.service'

__doc__ = """
Usage: cobra [command]

Commands:

 start/stop/status - Cobra Sentinel service control
 config            - Open configuration interface
"""

def main():
    if len(argv) < 2 or len(argv) > 2:
        print(__doc__)
    else:
        if argv[1] in ('start', 'stop', 'status'):
            system(CONTROL.format(argv[1]))
        elif argv[1] == 'config':
            config_main()
        else:
            raise Warning('Unknown argument')

if __name__ == "__main__":
    main()
