# CSC 445 - Assignment 1
# server.py

import socket

def test_latency(lat_data, sock):
    data_len = len(lat_data)
    lat_reply = bytearray()

    i = 0
    lat_reply.append(1)

    if data_len != 1:
        i += 1
        while i < data_len - 1:
            lat_reply.append(0)
            i += 1

            lat_reply.append(255)
            i += 1

    print "Sending latency reply..."
    amount_sent = 0
    while amount_sent < len(lat_reply):
        sent = sock.send(lat_reply[amount_sent:])
        amount_sent += sent
        print "** Sent " + str(sent) + " of " + str(len(lat_reply)) + "..."

    print "Reply sent..."

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket object for the server
port = 2694 # The port number assigned in class
buf_size = 8192 # Size of the receiving buffer

print "Starting server..."

# Start the server
serversocket.bind((socket.gethostname(), port))
serversocket.listen(5)

print "Server started on port " + str(port) + ". Host: " + str(socket.gethostname())

# The server loop
while 1:
    # Wait for connection
    print "Waiting for connection..."
    (client_socket, client_addr) = serversocket.accept()

    # Receive data from the connection
    print "Connection received from " + str(client_addr)
    data_bytes = []
    data = client_socket.recv(buf_size)
    while data != '':
        data_bytes.append(bytearray(data))
        data = client_socket.recv(buf_size)

    option = data_bytes[0][0]

    print repr(option)
    if option == 1:
        print "Latency test received"
        test_latency(data_bytes, client_socket)
    elif option == 2:
        print "Second option"
    else:
        print "No idea..."


client_socket.close()









