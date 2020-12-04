#!/usr/bin/env python3
from sys import argv
from os import system
from libconfig import main as config_main

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
