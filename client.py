# CSC 445 - Assignment 1
# client.py

import sys
import socket
import time
from socket_helper import fresh_socket


"""
    Methods start here
"""

def send_latency(s_lat_len, s_lat_sock):
    i = 0

    tp_array = bytearray()
    tp_array.append(1)
    i += 1

    while i < s_lat_len - 1:
        tp_array.append(0)
        i += 1

    if s_lat_len != 1:
        tp_array.append(255)

    amount_sent = 0
    while amount_sent < len(tp_array):
        sent = s_lat_sock.send(tp_array[amount_sent:])
        amount_sent += sent

    s_lat_sock.shutdown(socket.SHUT_RD)
    return time.clock()

def receive_latency(r_lat_len, r_lat_sock):
    received_bytes = []

    data = r_lat_sock.recv(r_lat_len)
    while data != '':
        received_bytes.append(bytes(data))
        data = r_lat_sock.recv(r_lat_len)

    r_lat_sock.close()
    return time.clock()



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



