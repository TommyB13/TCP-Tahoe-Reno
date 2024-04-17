import socket
import sys
import random

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 3021
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    
    print('Ready to serve...')

    while True:
        connection_socket, addr = server_socket.accept()
        try:
            message = connection_socket.recv(1024).decode()
            filename = message.split()[1][1:]

            with open(filename, "rb") as f:
                outputdata = f.read()

            # Simulate random packet drops
            if random.random() < 0.3:
                print("Simulating packet drop")
                continue  # Skip sending the response

            connection_socket.send(b"HTTP/1.1 200 OK\r\n\r\n" + outputdata)

        except IOError:
            # Send response message for file not found
            not_found_response = b"HTTP/1.1 404 Not Found\r\n\r\n<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
            connection_socket.send(not_found_response)

        finally:
            connection_socket.close()

    server_socket.close()

if __name__ == "__main__":
    main()