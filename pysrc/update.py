#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import basename
from os.path import join as path_join
from time import sleep
from urllib.request import urlretrieve
from config import AV_SOURCES, CHECK_FOR_UPDATES, DB_PATH, UPDATE_FREQ
from libavctl import send_reload


def main(show_output: bool = False) -> None:
    for i in AV_SOURCES:
        if show_output:
            print('Updating', basename(i))
        try:
            urlretrieve(i, path_join(DB_PATH, basename(i)))
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
    send_reload()
    print('Sent reload signal to daemon', flush=True)


if __name__ == '__main__':
    if CHECK_FOR_UPDATES:
        main()
    else:
        print('Updates disabled. Exiting.')
        exit()
    print(f'Sleeping {UPDATE_FREQ.pprint()}', flush=True)
    try:
        sleep(int(UPDATE_FREQ))
    except KeyboardInterrupt:
        print('Shutting down')
