import socket
import sys
import random
import time
from time import sleep
from colorama import Fore, Back, Style

class TCPSender:
    def __init__(self, filename):
        self.filename = filename
        self.host = "localhost"
        self.port = 3021
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender_socket.connect((self.host, self.port))
        self.seq_number = 0
        self.ack_number = 0
        self.cwnd = 1
        self.ssthresh = 64
        self.timeout = 2.0
        self.packet_size = 1024
        self.dup_ack_count = 0
        self.congestion_detected = False
        self.packets_sent = 0
        self.packets_lost = 0
        self.start_time = 0
        self.end_time = 0
        self.total_bytes_sent = 0

    def send_file(self):
        self.start_time = time.time()  # Record start time
        self.total_bytes_sent = 0

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
                if(random.randint(0, 10) < 9):
                    self.sender_socket.send(packet)
                    self.packets_sent += 1
                    self.total_bytes_sent += len(segment)
                    print(Fore.LIGHTGREEN_EX + f"Sent packet SEQ: {self.seq_number}" + Style.RESET_ALL)

                    # Adjust congestion window
                    if self.cwnd < self.ssthresh:
                        self.cwnd *= 2  # Exponential increase during slow start
                        print(f"Slow start, cwnd: {self.cwnd}, ssthresh: {self.ssthresh}")
                    else:
                        self.cwnd += 1  # Incremental increase during congestion avoidance
                        print(f"Congestion avoidance, cwnd: {self.cwnd}, ssthresh: {self.ssthresh}")
                else:
                    print(Fore.YELLOW + f"Packet loss, packet with SEQ: {self.seq_number} lost in transit." + Style.RESET_ALL)
                    self.packets_lost += 1
                    sleep(2)  # Simulate packet loss
                    continue  # Skip updating cwnd and ssthresh on packet loss

                if self.wait_for_ack():
                    print(Fore.LIGHTGREEN_EX + f"Received correct ACK: {self.ack_number}" + Style.RESET_ALL)
                    idx_packet += 1  # Successfully move to the next segment
                else:
                    self.ssthresh = max(self.cwnd / 2, 1) # Set slow start threshold to half of current cwnd
                    self.cwnd = 1
                    idx_packet = idx_packet - self.cwnd + 1 if idx_packet > 0 else 0
                    self.packets_lost += 1
                    print(f"Setting sshtresh to: {self.ssthresh} and cwnd to: {self.cwnd} due to timeout or incorrect ACK.")

        self.end_time = time.time()  # Record end time
        self.transmission_time = self.end_time - self.start_time
        self.throughput = self.total_bytes_sent / self.transmission_time

        print(f"Total bytes sent: {self.total_bytes_sent}")
        print(f"Total time taken: {round(self.transmission_time, 2)} seconds")
        print(f"Throughput: {round(self.throughput, 2)} bytes/second")

    def wait_for_ack(self):
        try:
            self.sender_socket.settimeout(self.timeout)
            response = self.sender_socket.recv(1024).decode()
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
            print(Fore.YELLOW + f'Timeout, resending last packet with SEQ: {self.seq_number}' + Style.RESET_ALL)
        except ValueError:
            print(Fore.YELLOW + f'Failed to convert ACK to integer.' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.YELLOW + f"Unexpected error: {e}" + Style.RESET_ALL)
        return False

    def close(self):
        self.sender_socket.close()
        print("Total packets sent: ", self.packets_sent, " Total packets lost: ", self.packets_lost)
        print("Goodput: ", self.packets_sent - self.packets_lost, "/", self.packets_sent, "|", round((self.packets_sent - self.packets_lost) / self.packets_sent * 100, 2), "%)")
        print(Fore.CYAN + "Connection closed with receiver" + Style.RESET_ALL)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sender.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    sender = TCPSender(filename)
    sender.send_file()
    sender.close()
