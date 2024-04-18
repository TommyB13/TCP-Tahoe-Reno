#!/bin/bash

# Function to print separator lines
print_separator() {
    echo "====================="
}

# Start the server
print_separator
echo "Starting server..."
python3 ./tahoe-final/server_tahoe_only.py &
server_pid=$!

# Wait for a moment to ensure server startup
sleep 2

# Run the client
print_separator
echo "Running client..."
python3 ./tahoe-final/client_tahoe-only2.py

# Stop the server after the client finishes
print_separator
echo "Stopping server..."
kill $server_pid
