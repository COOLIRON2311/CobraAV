#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gc import collect
from os.path import basename
from os.path import join as path_join
from time import sleep
from requests import get
from config import AV_SOURCES, CHECK_FOR_UPDATES, DB_PATH, UPDATE_FREQ


def main() -> None:
    for i in AV_SOURCES:
        r = get(i, allow_redirects=True)
        with open(path_join(DB_PATH, basename(i)), 'wb') as f:
            f.write(r.content)
    print(f'Freed {collect()} bytes')


if __name__ == '__main__':
    if CHECK_FOR_UPDATES:
        main()
    print(f'Sleeping {UPDATE_FREQ.pprint()}')
    try:
        sleep(UPDATE_FREQ.value)
    except KeyboardInterrupt:
        print('Shutting down')
