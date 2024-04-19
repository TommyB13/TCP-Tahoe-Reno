from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
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
            except timeout:
                break
        connectionSocket.close()
    except IOError:
        not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        not_found_response += "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
        connectionSocket.sendall(not_found_response.encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()

