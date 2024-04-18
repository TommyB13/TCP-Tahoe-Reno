import socket
import random
from colorama import Fore, Back, Style

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 3021
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    
    print(f'Server is ready to receive on port {server_port}')
    while True:
        connection_socket, addr = server_socket.accept()
        print(Fore.CYAN + f'Connection established with {addr}' + Style.RESET_ALL)
        
        try:
            cwnd = 1  # Initialize congestion window
            ssthresh = 64  # Initialize slow start threshold
            last_ack_seq_num = 0  # Initialize last acknowledged sequence number
            duplicate_ack_count = 0  # Initialize duplicate ACK count
            
            with open('output.html', 'wb') as file:
                while True:
                    packet = connection_socket.recv(2048)
                    if not packet:
                        print("No more data received.")
                        break
                    header, data_content = packet.split(b'|DATA:', 1)
                    seq_num = int(header.decode().split('SEQ:')[1].split('|')[0])
                    ack_num = int(header.decode().split('ACK:')[1].split('|')[0])  # Extract ACK number
                    
                    # Write received data into the file
                    file.write(data_content)
                    
                    print(Fore.LIGHTGREEN_EX + f"Received packet with SEQ: {seq_num}" + Style.RESET_ALL, flush=True )
                    ack_response = seq_num + len(data_content)
                    
                    # Simulate packet loss with probability 20%
                    if (random.randint(0, 10) < 9):
                        connection_socket.send(f"SEQ:{seq_num}|ACK:{ack_response}|DATA:".encode())
                        print(Fore.LIGHTGREEN_EX + f"Sent ACK: {ack_response}" + Style.RESET_ALL, flush=True)
                    else:
                        print(Fore.YELLOW + f"Packet loss, no ACK sent with ACK {ack_response}" + Style.RESET_ALL, flush=True)
                        continue  # Skip updating cwnd and ssthresh on packet loss
                    
                    # Congestion control
                    if ack_num >= seq_num:
                        if not ssthresh:
                            cwnd = min(cwnd * 2, 64)  # Slow start
                        else:
                            cwnd += 1  # Congestion avoidance
                    
                    # Detect and simulate three duplicate ACKs
                    if ack_num < seq_num and ack_num != last_ack_seq_num:
                        duplicate_ack_count += 1
                        if duplicate_ack_count == 3:
                            # Send three duplicate ACKs
                            for _ in range(3):
                                connection_socket.send(f"SEQ:{last_ack_seq_num}|ACK:{ack_response}|DATA:".encode())
                                print(f"Sent duplicate ACK for SEQ: {last_ack_seq_num}", flush=True)
                            duplicate_ack_count = 0  # Reset duplicate ACK count
                    else:
                        duplicate_ack_count = 0  # Reset duplicate ACK count`


                    last_ack_seq_num = ack_num  # Update last acknowledged sequence number

                    # Detect and simulate three duplicate ACKs... USE FOR DEMONSTRATION OF DUPLICATE ACK ONLY
                    if ack_num == last_ack_seq_num:
                        duplicate_ack_count += 1
                        if duplicate_ack_count == 3:
                            # Send three duplicate ACKs
                            for _ in range(3):
                                connection_socket.send(f"SEQ:{last_ack_seq_num}|ACK:{ack_response}|DATA:".encode())
                                print(f"Sent duplicate ACK for SEQ: {last_ack_seq_num}", flush=True)
                            duplicate_ack_count = 0  # Reset duplicate ACK count
                    else:
                        duplicate_ack_count = 0  # Reset duplicate ACK count if the ACK is not a duplicate


        finally:
            connection_socket.close()
            print(Fore.CYAN + "Connection closed with client." + Style.RESET_ALL)

    server_socket.close()

if __name__ == "__main__":
    main()
