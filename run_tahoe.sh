#!/bin/bash

# Function to print separator lines
print_separator() {
    echo "====================="
}

# Start the receiver
print_separator
echo "Starting Tahoe receiver..."
python3 ./tahoe-final/receiver_tahoe_only.py &
receiver_pid=$!

# Wait for a moment to ensure receiver startup
sleep 2

# Run the client
print_separator
echo "Running Tahoe sender..."
python3 ./tahoe-final/sender_tahoe_only2.py ./inputs/lorem_ipsum.txt

# Stop the receiver after the sender finishes
print_separator
echo "Stopping Tahoe receiver..."
kill $receiver_pid
