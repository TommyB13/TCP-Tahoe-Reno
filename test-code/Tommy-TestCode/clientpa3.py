import socket
import sys
import time

class TCPClient:
    def __init__(self, host, port, filename):
        self.host = host
        self.port = port
        self.filename = filename
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.packets_sent = 0
        self.packets_lost = 0
        self.packets_received = 0
        self.start_time = 0
    
    def connect(self):
        self.client_socket.connect((self.host, self.port))
    
    def send_request(self):
        request = f"GET /{self.filename} HTTP/1.1\r\nHost: {self.host}\r\nConnection: close\r\n\r\n"
        self.client_socket.send(request.encode())
        self.packets_sent += 1
    
    def receive_response(self):
        response = b""
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            response += data
        self.packets_received += 1
        return response.decode("utf-8")
    
    def close(self):
        self.client_socket.close()
    
    def calculate_performance(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        throughput = self.packets_received / total_time
        goodput = self.packets_received / self.packets_sent
        return throughput, goodput

class TCPClientTahoe(TCPClient):
    def __init__(self, host, port, filename):
        super().__init__(host, port, filename)
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
    
    def send_request(self):
        self.connect()
        super().send_request()
        response = self.receive_response()
        print("Response from server:")
        print(response)
        self.close()

class TCPClientReno(TCPClientTahoe):
    def __init__(self, host, port, filename):
        super().__init__(host, port, filename)
    
    def congestion_control(self):
        if self.dupack == 3:
            self.ssthresh = self.cwnd / 2
            self.cwnd = self.ssthresh
            self.send_request()
            self.next += 1
        else:
            self.dupack = 0

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 http_client.py <host> <port> <filename> <algorithm>")
        print("Algorithm: tahoe or reno")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    algorithm = sys.argv[4].lower()
    
    if algorithm == 'tahoe':
        client = TCPClientTahoe(host, port, filename)
    elif algorithm == 'reno':
        client = TCPClientReno(host, port, filename)
    else:
        print("Invalid algorithm. Please choose 'tahoe' or 'reno'.")
        sys.exit(1)
    
    client.start_time = time.time()
    client.send_request()
    throughput, goodput = client.calculate_performance()
    print(f"Throughput: {throughput} packets/sec")
    print(f"Goodput: {goodput}")

