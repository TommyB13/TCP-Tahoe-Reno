#!/bin/bash

# Function to print separator lines
print_separator() {
    echo "====================="
}

# Start the Reno server
print_separator
echo "Starting Reno server..."
python3 ./reno-final/server_reno_only.py &
server_pid=$!

# Wait for a moment to ensure server startup
sleep 2

# Run the Reno client
print_separator
echo "Running Reno client..."
python3 ./reno-final/client_reno_only.py ./inputs/lorem_ipsum.txt

# Stop the Reno server after the client finishes
print_separator
echo "Stopping Reno server..."
kill $server_pid
