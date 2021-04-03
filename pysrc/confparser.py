#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import *

args = f'-msize {MAX_FILE_SIZE} -threat {REMOVE_THREATS} -t {" ".join(SCAN_TARGETS)} -e {" ".join(SCAN_EXCLUDE)} -q {QUARANTINE_PATH}'

def main() -> None:
    """
Parser arguments docs:
----------------------

-msize - Max files size to scan (in bytes). Files of greater size will be ignored.
-threat - Action on threat detection:
          0 - Move threat to quarantine
          1 - Remove infected file
-t - Scan target directories recursively
-e - Exclude files and directories from scan query by wildcard
-q - Quarantine directory path
"""
    print(args)

if __name__ == '__main__':
    main()
