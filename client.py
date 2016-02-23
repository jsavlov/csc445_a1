# CSC 445 - Assignment 1
# client.py

import sys
import socket
import time


"""
    Methods start here
"""

def send_latency(tp_len, tp_sock):
    i = 0

    tp_array = bytearray()
    tp_array.append(1)
    i += 1

    while i < tp_len - 1:
        tp_array.append(0)
        i += 1

    if tp_len != 1:
        tp_array.append(255)

    amount_sent = 0
    while amount_sent < len(tp_array):
        sent = tp_sock.send(tp_array[amount_sent:])
        amount_sent += sent

    tp_sock.shutdown(socket.SHUT_RD)
    return time.clock()

def receive_latency(lat_len, lat_sock):
    received_bytes = []

    data = lat_sock.recv(lat_len)
    while data != '':
        received_bytes.append(bytes(data))
        data = lat_sock.recv(lat_len)

    lat_sock.close()
    return time.clock()

def fresh_socket(host, port):
    f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # The socket object used to connect to the server

    print "Opening connection to host " + str(host) + " on port " + str(port) + "..."

    # Open the connection
    f_socket.connect((host, port))

    print "Connection opened."

    return f_socket


"""
    This is where the program script starts
"""

# If there was a server entered as a command line argument,
# use that one.
try:
    HOST_SERVER = sys.argv[1]
except IndexError:
    HOST_SERVER = raw_input("Enter the host server address: ")

PORT = 2694  # The port used for the socket


host_socket = fresh_socket(HOST_SERVER, PORT)
print "Sending Latency Test: 1 byte"
lat1_tx_time = send_latency(1, host_socket)
lat1_rx_time = receive_latency(1, host_socket)
lat1_rtt_time = lat1_rx_time - lat1_tx_time
print "Latency 1 byte result: " + str(lat1_rtt_time * 1000)

host_socket = fresh_socket(HOST_SERVER, PORT)
print "Sending Latency Test: 32 bytes"
lat32_tx_time = send_latency(32, host_socket)
lat32_rx_time = receive_latency(32, host_socket)
lat32_rtt_time = lat32_rx_time - lat32_tx_time
print "Latency 32 byte result: " + str(lat32_rtt_time * 1000)

host_socket = fresh_socket(HOST_SERVER, PORT)
print "Sending Latency Test: 1024 bytes"
lat1024_tx_time = send_latency(1024, host_socket)
host_socket.recv(1024)
lat1024_rx_time = receive_latency(1024, host_socket)
lat1024_rtt_time = lat1024_rx_time - lat1024_tx_time
print "Latency 1024 byte result: " + str(lat1024_rtt_time * 1000)


# Close the connection
host_socket.close()



