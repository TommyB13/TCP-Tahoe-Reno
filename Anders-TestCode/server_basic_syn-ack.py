import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 3021
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    
    print(f'Server is ready to receive on port {server_port}')
    while True:
        connection_socket, addr = server_socket.accept()
        print(f'Connection established with {addr}')
        
        try:
            with open('output.html', 'wb') as file:
                while True:
                    packet = connection_socket.recv(2048)
                    if not packet:
                        print("No more data received.")
                        break
                    header, data_content = packet.split(b'|DATA:', 1)
                    seq_num = int(header.decode().split('SEQ:')[1].split('|')[0])
                    
                    # Write received data into the file
                    file.write(data_content)
                    
                    print(f"Received packet with SEQ: {seq_num}", flush=True)
                    ack_response = seq_num + len(data_content)
                    response = f"SEQ:{seq_num}|ACK:{ack_response}|DATA:".encode()
                    connection_socket.send(response)
                    print(f"Sent ACK: {ack_response}", flush=True)
                    
        finally:
            connection_socket.close()
            print("Connection closed with client.")

    server_socket.close()

if __name__ == "__main__":
    main()