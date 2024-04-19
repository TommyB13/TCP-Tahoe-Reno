import socket
import sys
import time
import random

class TCPClient:
    def __init__(self, filename):
        self.host = "localhost"
        self.port = 3021
        self.filename = filename
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.total_packets_sent = 0
        self.good_packets_received = 0
        self.start_time = 0
    
    def connect(self):
        self.client_socket.connect((self.host, self.port))
    
    def send_request(self, timeout=5):
        request = f"GET /{self.filename} HTTP/1.1\r\nHost: {self.host}\r\nConnection: close\r\n\r\n"
        self.client_socket.send(request.encode())
        self.total_packets_sent += 1
        self.client_socket.settimeout(timeout)
    
    def receive_response(self):
        response = b""
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                response += data
            except socket.timeout:
                print("Timeout occurred while receiving response.")
                break
        if "HTTP/1.1 200 OK" in response.decode("utf-8"):
            self.good_packets_received += 1
        return response.decode("utf-8")
    
    def close(self):
        self.client_socket.close()
    
    def calculate_performance(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        throughput = self.good_packets_received / total_time
        goodput = self.good_packets_received / self.total_packets_sent if self.total_packets_sent > 0 else 0
        return throughput, goodput, self.total_packets_sent, self.good_packets_received

class TCPClientTahoe(TCPClient):
    def __init__(self, filename):
        super().__init__(filename)
        self.cwnd = 1
        self.ssthresh = 32
        self.max_cwnd = 50
        self.una = 0
        self.next = 1
        self.dupack = 0
    
    def congestion_control(self):
        if self.dupack == 3:
            self.ssthresh = self.cwnd / 2
            self.cwnd = 1
            self.next = self.una
            self.send_request()
            self.next += 1
        else:
            self.dupack = 0
    
    def send_request(self, timeout=5):
        self.connect()
        super().send_request(timeout)
        response = self.receive_response()
        expected_response = "HTTP/1.1 200 OK"
        if expected_response not in response:
            print("Unexpected response:", response)
        else:
            print("Response from server:")
            print(response)
        self.close()

class TCPClientReno(TCPClientTahoe):
    def __init__(self, filename):
        super().__init__(filename)
    
    def congestion_control(self):
        if self.dupack == 3:
            self.ssthresh = self.cwnd / 2
            self.cwnd = self.ssthresh
            self.send_request()
            self.next += 1
        else:
            self.dupack = 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 http_client.py <filename> <algorithm>")
        print("Algorithm: tahoe or reno")
        sys.exit(1)
    
    filename = sys.argv[1]
    algorithm = sys.argv[2].lower()
    
    if algorithm == 'tahoe':
        client = TCPClientTahoe(filename)
    elif algorithm == 'reno':
        client = TCPClientReno(filename)
    else:
        print("Invalid algorithm. Please choose 'tahoe' or 'reno'.")
        sys.exit(1)
    
    client.start_time = time.time()
    client.send_request()
    throughput, goodput, total_packets_sent, good_packets_received = client.calculate_performance()
    print(f"Throughput: {throughput} packets/sec")
    print(f"Goodput: {goodput}")
    print(f"Total packets sent: {total_packets_sent}")
    print(f"Good packets received: {good_packets_received}")
