#!/bin/bash

# Function to print separator lines
print_separator() {
    echo "====================="
}

# Start the Reno receiver
print_separator
echo "Starting Reno receiver..."
python3 ./reno-final/receiver_reno_only.py &
server_pid=$!

# Wait for a moment to ensure receiver startup
sleep 2

# Run the Reno client
print_separator
echo "Running Reno sender..."
python3 ./reno-final/sender_reno_only.py ./inputs/lorem_ipsum.txt

# Stop the Reno receiver after the client finishes
print_separator
echo "Stopping Reno receiver..."
kill $server_pid
