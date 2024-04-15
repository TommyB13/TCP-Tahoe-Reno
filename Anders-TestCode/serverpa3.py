import socket
import sys
import random

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverPort = 3021
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1][1:]
        print("Filename requested:", filename)
        with open(filename, "rb") as f:
            outputdata = f.read()
        
        # Simulate random packet drops (drop 30% of packets)
        if random.random() < 0.3:
            print("Simulating packet drop")
            continue  # Skip sending the response
        
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        connectionSocket.sendall(outputdata)
        
        # Simulate TCP Tahoe behavior
        # if duplicate Acks are received, close the connection
        for _ in range(3):
            connectionSocket.settimeout(0.5)
            try:
                ack = connectionSocket.recv(1024)
                if not ack:
                    break
            except socket.timeout:
                break
        connectionSocket.close()
    except IOError:
        not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        not_found_response += "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
        connectionSocket.sendall(not_found_response.encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()
