import socket
import sys
import time

class TCPClient:
    def __init__(self, filename):
        self.host = "localhost"
        self.port = 3021
        self.filename = filename
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.total_packets_sent = 0
        self.good_packets_received = 0
        self.start_time = 0
        self.seq_number = 0
        self.ack_number = 0
        self.cwnd = 1
        self.ssthresh = 64

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send_request(self):
        request = f"GET /{self.filename} HTTP/1.1\r\nHost: {self.host}\r\nConnection: close\r\n\r\n"
        self.client_socket.send(request.encode())
        self.total_packets_sent += 1

    def receive_response(self):
        response = b""
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                response += data
        except socket.timeout:
            print("Timeout occurred while receiving response.")
        return response.decode("utf-8")

    def calculate_performance(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        throughput = self.good_packets_received / total_time if total_time > 0 else 0
        goodput = (self.good_packets_received / self.total_packets_sent) if self.total_packets_sent > 0 else 0
        return throughput, goodput, self.total_packets_sent, self.good_packets_received

    def close(self):
        self.client_socket.close()


class TCPClientTahoe(TCPClient):
    def __init__(self, filename):
        super().__init__(filename)
    
    def send_request(self):
        super().send_request()
        print("Using Tahoe: Slow start and congestion avoidance only.")

    def adjust_cwnd_for_packet_loss(self):
        self.ssthresh = max(self.cwnd / 2, 2)  # ssthresh is max of half of cwnd or 2
        self.cwnd = 1                        # Restart cwnd from 1 (Slow start)

class TCPClientReno(TCPClient):
    def __init__(self, filename):
        super().__init__(filename)

    def send_request(self):
        super().send_request()
        print("Using Reno: Includes Fast Recovery.")

    def adjust_cwnd_for_3_dup_acks(self):
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = self.ssthresh  # Fast recovery: cwnd is set to ssthresh

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tcp_client.py <filename> <algorithm>")
        sys.exit()

    filename = sys.argv[1]
    algorithm = sys.argv[2].lower()
    
    if algorithm == 'tahoe':
        client = TCPClientTahoe(filename)
    elif algorithm == 'reno':
        client = TCPClientReno(filename)
    else:
        print("Invalid algorithm. Please choose 'tahoe' or 'reno'.")
        sys.exit()
    
    client.start_time = time.time()
    client.connect()
    client.send_request()
    response = client.receive_response()
    print("Response from server:")
    print(response)
    throughput, goodput, total_packets_sent, good_packets_received = client.calculate_performance()
    print(f"Throughput: {throughput} packets/sec")
    print(f"Goodput: {goodput}")
    print(f"Total packets sent: {total_packets_sent}")
    print(f"Good packets received: {good_packets_received}")
    client.close()