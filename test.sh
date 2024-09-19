#!/bin/bash

# Function to print messages in both English and Japanese
print_message() {
    echo "$1"
    echo "$2"
    echo ""
}

# Function to run a test and measure time
run_test() {
    start_time=$(date +%s.%N)
    $1 > /dev/null 2>&1
    end_time=$(date +%s.%N)
    echo "$(echo "$end_time - $start_time" | bc) seconds"
}

print_message "Starting performance test..." ""

# CPU Test
print_message "CPU Test: Calculate prime numbers" ""
cpu_time=$(run_test "seq 1 20000 | factor | wc -l")
print_message "CPU Test completed in: $cpu_time" ""

# Memory Test
print_message "Memory Test: Sort a large array" ""
memory_time=$(run_test "sort -R <(seq 1 1000000) > /dev/null")
print_message "Memory Test completed in: $memory_time" ""

# Disk I/O Test
print_message "Disk I/O Test: Write and read a large file" ""
io_time=$(run_test "dd if=/dev/zero of=test_file bs=1M count=1024 && sync && dd if=test_file of=/dev/null bs=1M && rm test_file")
print_message "Disk I/O Test completed in: $io_time" ""
