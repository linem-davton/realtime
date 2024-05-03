#!/bin/bash

# Define a temporary source file
SOURCE_FILE=$(mktemp /tmp/clock_getres.XXXXXX.c)

# Create a C program to get clock resolutions
cat <<EOF >$SOURCE_FILE
#include <stdio.h>
#include <time.h>

void print_clock_res(clockid_t clk_id, const char* name) {
    struct timespec res;
    clock_getres(clk_id, &res);
    printf("%s resolution: %ld seconds, %ld nanoseconds\\n", name, res.tv_sec, res.tv_nsec);
}

int main() {
    print_clock_res(CLOCK_REALTIME, "CLOCK_REALTIME");
    print_clock_res(CLOCK_MONOTONIC, "CLOCK_MONOTONIC");
    return 0;
}
EOF

# Compile the C program
gcc -o /tmp/clock_getres $SOURCE_FILE

# Run the compiled program
/tmp/clock_getres

# Clean up
rm $SOURCE_FILE /tmp/clock_getres
