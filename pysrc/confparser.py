#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import *

args = f'-msize {MAX_FILE_SIZE} -threat {REMOVE_THREATS} -t {" ".join(SCAN_TARGETS)} -e {" ".join(SCAN_EXCLUDE)} -q {QUARANTINE_PATH}'

def main() -> None:
    print(args)

if __name__ == '__main__':
    main()
