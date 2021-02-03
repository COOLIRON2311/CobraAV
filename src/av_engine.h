#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <clamav.h>

/*
 * Exit codes:
 *  0: clean
 *  1: infected
 *  2: error
 */

int setup();
int scan(const char*);
