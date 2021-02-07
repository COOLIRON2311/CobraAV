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
FIFO_PATH = '/tmp/cobra.sock'

__doc__ = """
Usage: cobra [command] [file]

Commands:

 start/stop/status - Cobra Sentinel service control (reqires root)
 (de)contain       - Move file from/to quarantine
 remove            - Delete contained threat
 config            - Open configuration interface
 scan              - Manually specify scan target
 whitelist         - Add file signature to exceptions list
 blacklist         - Add file signature to malware database
 list-threats      - View contained threats
 clear-threats     - Delete all contained threats
"""


def __get_new_name(path: str) -> str:
    ret = 0
    name = basename(path)
    for i in scandir(QUARANTINE_PATH):
        if name in i.name and '.avmeta' not in i.path:
            ret += 1
    return '' if not ret else f'.{ret}'


def __read_meta(raw_path: str) -> str:
    with open(raw_path + '.avmeta', 'r') as f:
        return f.read().splitlines()


def contain(path: str) -> None:
    path = abspath(path)
    out = path_join(QUARANTINE_PATH, basename(path) + __get_new_name(path))
    if not isfile(path):
        raise FileNotFoundError('path is not a file')
    rename(path, out)
    with open(out + '.avmeta', 'w') as f:
        f.write(path + '\n')
        f.write(str(stat(out).st_mode))
    chmod(out, 0)


def decontain(name: str) -> None:
    out = path_join(QUARANTINE_PATH, name)
    if not isfile(out):
        raise FileNotFoundError
    path, mod = __read_meta(out)
    if isfile(path):
        raise FileExistsError('file exists in target location')
    rename(out, path)
    chmod(path, int(mod))
    remove(out + '.avmeta')


def _remove(name: str) -> None:
    path = path_join(QUARANTINE_PATH, name)
    if isfile(path):
        remove(path)
    if isfile(path + 'out'):
        remove(path + '.avmeta')


def list_threats() -> None:
    try:
        width = max(len('%i' % getsize(i)) for i in scandir(QUARANTINE_PATH))
    except ValueError:
        return
    for i in scandir(QUARANTINE_PATH):
        if '.avmeta' not in i.path:
            st = stat(i.path)
            _, mod = __read_meta(i.path)
            ctime = datetime.fromtimestamp(getctime(i.path + '.avmeta')).strftime(r'%b %d %Y %H:%M')
            print(f'{filemode(int(mod))} {getpwuid(st.st_uid).pw_name} {st.st_size:>{width}} {ctime} {basename(i)}')


def clear_threats() -> None:
    for i in scandir(QUARANTINE_PATH):
        remove(i.path)


def main() -> None:
    argc = len(argv)
    if argc < 2:
        print(__doc__)

    elif argc == 2:
        opts = {'config': config_main, 'list-threats': list_threats,
                'clear-threats': clear_threats}
        if argv[1] in ('start', 'stop', 'status'):
            system(CONTROL.format(argv[1]))
        elif argv[1] in opts:
            opts[argv[1]]()
        else:
            raise InvalidArgument

    elif argc == 3:
        opts = {'whitelist': DataBase.whitelist,
                'blacklist': DataBase.blacklist,
                'scan': lambda x: enqueue_scan(abspath(x), FIFO_PATH),
                'contain': contain,
                'decontain': decontain,
                'remove': _remove}
        if argv[1] in opts:
            opts[argv[1]](argv[2])
        else:
            raise InvalidArgument
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
