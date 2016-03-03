# CSC 445 - Assignment 1
# server.py

import socket
import getopt
import sys
from socket_helper import fresh_server_socket
from socket_functions import test_latency, test_throughput, test_interaction


port = 2694 # The port number assigned in class
buf_size = 4096 # Size of the receiving buffer

# A usage message to help users who are unfamiliar with the program
usage = "Usage: server.py -p <tcp | udp>"

try:
    opts, args = getopt.getopt(sys.argv[1:], "p:")
except getopt.GetoptError:
    print str(usage)
    sys.exit(2)

if len(opts) == 0:
    using_udp = False

for opt, arg in opts:
    if opt == '-p':
        pro_choice = arg
        if arg == "udp":
            using_udp = True
            print "Using UDP..."
        elif arg == "tcp":
            using_udp = False
            print "Using TCP..."
        else:
            print str(usage)
            sys.exit(2)


print "Starting server..."

# Create a server socket
serversocket = fresh_server_socket(port, using_udp)

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
    incoming_interaction_test = False
    while data != '' or incoming_interaction_test is True:
        data_bytes.append(bytearray(data))
        if data_bytes[0][0] == 3 and incoming_interaction_test is False:
            incoming_interaction_test = True

        if incoming_interaction_test is True:
            d_len = len(data)
            if ord(data[d_len - 1]) == 255:
                break
        data = client_socket.recv(buf_size)

    option = data_bytes[0][0]

    print repr(option)
    if option == 1:
        print "Latency test received"
        test_latency(data_bytes, client_socket)
    elif option == 2:
        print "Throughput test received"
        test_throughput(data_bytes, client_socket)
    elif option == 3:
        print "Interaction test received"
        test_interaction(client_socket)
    else:
        print "No idea..."


client_socket.close()
