import socket
import sys
import time

class TCPClient:
    def __init__(self, filename):
        self.filename = filename
        self.host = "localhost"
        self.port = 3021
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.seq_number = 0
        self.ack_number = 0
        self.timeout = 1.0
        self.buffer_size = 1024
        self.cwnd = 1
        self.ssthresh = 64

    def send_file(self):
        try:
            with open(self.filename, 'rb') as file:
                data = file.read()
                total_packets = len(data) // self.buffer_size + (len(data) % self.buffer_size != 0)
                packets = [
                    data[i * self.buffer_size: (i+1) * self.buffer_size]
                    for i in range(total_packets)
                ]
                idx = 0
                duplicate_acks = 0
                while idx < len(packets):
                    if idx < self.cwnd:
                        segment = packets[idx]
                        self.seq_number += len(segment)
                        packet = f"SEQ:{self.seq_number}|ACK:{self.ack_number}|DATA:".encode() + segment
                        self.client_socket.send(packet)
                        print(f"Sent packet SEQ: {self.seq_number}")
                        
                        if self.wait_for_ack():
                            idx += 1
                            duplicate_acks = 0  # reset upon new ack
                        else:
                            print("Timeout or duplicate ACK. Handling congestion control.")
                            self.cwnd = 1
                            self.ssthresh = max(self.cwnd / 2, 1)
                            idx = idx - duplicate_acks
                            duplicate_acks += 1
        finally:
            self.close()

    def wait_for_ack(self):
        try:
            self.client_socket.settimeout(self.timeout)
            response = self.client_socket.recv(1024).decode()
            ack_response = int(response.split('|')[1].split('ACK:')[1].strip())
            
            if ack_response > self.ack_number:
                self.ack_number = ack_response
                return True
            else:
                return False
        except socket.timeout:
            print('Timeout, resending last packet...')
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def close(self):
        self.client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    client = TCPClient(filename)
    client.send_file()