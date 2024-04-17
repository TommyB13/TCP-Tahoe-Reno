import socket
import sys

class TCPClient:
    def __init__(self, filename):
        self.filename = filename
        self.host = "localhost"
        self.port = 3021
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.seq_number = 0
        self.ack_number = 0
        self.cwnd = 1
        self.ssthresh = 64
        self.timeout = 2.0
        self.packet_size = 1024

    def send_file(self):
        with open(self.filename, 'rb') as file:
            data = file.read()
            total_segments = len(data) // self.packet_size + (len(data) % self.packet_size != 0)
            idx_packet = 0

            while idx_packet < total_segments:
                start = idx_packet * self.packet_size
                end = start + self.packet_size
                segment = data[start:end]
                self.seq_number = end
                packet = f"SEQ:{self.seq_number}|ACK:{self.ack_number}|DATA:".encode() + segment
                self.client_socket.send(packet)
                print(f"Sent packet SEQ: {self.seq_number}")

                if self.wait_for_ack():
                    print(f"Received correct ACK: {self.ack_number}")
                    idx_packet += 1  # Successfully move to the next segment
                else:
                    print("Timeout or incorrect ACK. Handling congestion control.")
                    self.ssthresh = max(self.cwnd / 2, 1)
                    self.cwnd = 1
                    idx_packet = idx_packet - self.cwnd + 1 if idx_packet > 0 else 0

    def wait_for_ack(self):
        try:
            self.client_socket.settimeout(self.timeout)
            response = self.client_socket.recv(1024).decode()
            header = response.split('DATA:')[0]
            ack_num = int(header.split('ACK:')[1].split('|')[0])
            
            if ack_num >= self.seq_number:  # Check if received ACK is sufficient to cover last SEQ sent
                self.ack_number = ack_num
                return True
            else:
                print(f"Received insufficient ACK: {ack_num}, expected at least: {self.seq_number}")
                
        except socket.timeout:
            print('Timeout, resending last packet...')
        except ValueError:
            print('Failed to convert ACK to integer.')
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
    client.close()