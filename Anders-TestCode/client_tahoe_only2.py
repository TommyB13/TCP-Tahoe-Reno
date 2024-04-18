import socket
import sys
import random
import threading

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
        self.dup_ack_count = 0
        self.congestion_detected = False
        self.sent_packets = {}  # Dictionary to store sent packets and their associated timers
        self.lock = threading.Lock()

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
                
                # Send packet and start timer
                self.client_socket.send(packet)
                self.lock.acquire()
                self.sent_packets[self.seq_number] = threading.Timer(self.timeout, self.handle_timeout, args=[self.seq_number, packet])
                self.sent_packets[self.seq_number].start()
                self.lock.release()
                print(f"Sent packet SEQ: {self.seq_number}")
                
                idx_packet += 1  # Move to the next segment

        # Wait for ACKs of all sent packets before closing connection
        for seq_number, timer in self.sent_packets.items():
            timer.join()

    def wait_for_ack(self):
        try:
            self.client_socket.settimeout(self.timeout)
            response = self.client_socket.recv(1024).decode()
            header = response.split('DATA:')[0]
            ack_num = int(header.split('ACK:')[1].split('|')[0])
            
            if ack_num >= self.seq_number:  # Check if received ACK is sufficient to cover last SEQ sent
                self.ack_number = ack_num
                
                # Congestion detection
                if ack_num == self.seq_number:
                    self.dup_ack_count += 1
                    print(f"Received #{self.dup_ack_count} duplicate ACK for SEQ: {ack_num}")
                    if self.dup_ack_count == 3:  # Three duplicate ACKs
                        self.ssthresh = max(self.cwnd / 2, 1)
                        self.cwnd = 1
                        self.congestion_detected = True
                        print(f"Congestion with 3 duplicate ACKs detected, setting ssthresh to: {self.ssthresh} and cwnd to: {self.cwnd}")
                else:
                    self.dup_ack_count = 0  # Reset duplicate ACK count
                    
                return True
            else:
                print(f"Received insufficient ACK: {ack_num}, expected at least: {self.seq_number}")
                
        except socket.timeout:
            print('Timeout, resending last packet with SEQ:', self.seq_number)
        except ValueError:
            print('Failed to convert ACK to integer.')
        except Exception as e:
            print(f"Unexpected error: {e}")
        return False

    def handle_timeout(self, seq_number, packet):
        print(f"Timeout occurred for packet with SEQ: {seq_number}. Retransmitting...")
        # Resend packet
        self.client_socket.send(packet)
        # Restart timer
        self.lock.acquire()
        self.sent_packets[seq_number].cancel()
        self.sent_packets[seq_number] = threading.Timer(self.timeout, self.handle_timeout, args=[seq_number, packet])
        self.sent_packets[seq_number].start()
        self.lock.release()

    def close(self):
        # Cancel all timers
        for seq_number, timer in self.sent_packets.items():
            timer.cancel()
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
