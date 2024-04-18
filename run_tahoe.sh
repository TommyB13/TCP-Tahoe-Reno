#!/bin/bash

# Function to print separator lines
print_separator() {
    echo "====================="
}

# Start the server
print_separator
echo "Starting Tahoe server..."
python3 ./tahoe-final/server_tahoe_only.py &
server_pid=$!

# Wait for a moment to ensure server startup
sleep 2

# Run the client
print_separator
echo "Running Tahoe client..."
python3 ./tahoe-final/client_tahoe_only2.py ./inputs/lorem_ipsum.txt

# Stop the server after the client finishes
print_separator
echo "Stopping Tahoe server..."
kill $server_pid
