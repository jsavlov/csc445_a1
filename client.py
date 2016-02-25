# CSC 445 - Assignment 1
# client.py

import sys
import socket
import time
import getopt
from socket_helper import fresh_client_socket


"""
    Methods start here
"""

def send_latency(s_lat_len, s_lat_sock):
    i = 0

    lat_array = bytearray()
    lat_array.append(1)
    i += 1

    while i < s_lat_len - 1:
        lat_array.append(0)
        i += 1

    if s_lat_len != 1:
        lat_array.append(255)

    s_time = time.clock()
    amount_sent = 0
    while amount_sent < len(lat_array):
        sent = s_lat_sock.send(lat_array[amount_sent:])
        amount_sent += sent

    s_lat_sock.shutdown(socket.SHUT_RD)
    return s_time

def receive_latency(r_lat_len, r_lat_sock):
    received_bytes = []

    data = r_lat_sock.recv(r_lat_len)
    while data != '':
        received_bytes.append(bytes(data))
        data = r_lat_sock.recv(r_lat_len)

    r_time = time.clock()
    r_lat_sock.close()
    return r_time

def calc_throughput(tp_size, tp_sock):
    i = 0

    tp_array = bytearray()
    tp_array.append(2)

    while i < tp_size - 1:
        tp_array.append(0)
        i += 1

    if tp_size != 1:
        tp_array.append(255)
        i += 1

    s_time = time.clock()
    amount_sent = 0
    while amount_sent < len(tp_array):
        sent = tp_sock.send(tp_array[amount_sent:])
        amount_sent += sent

    tp_sock.shutdown(socket.SHUT_RD)

    reply_bytes = []

    data = tp_sock.recv(4096)
    while data != '':
        reply_bytes.append(data)
        data = tp_sock.recv(4096)

    r_time = time.clock()
    tp_sock.close()

    tx_time = (r_time + s_time) / 2

    tx_rate = tp_size / tx_time

    return tx_rate

"""
    This is where the program script starts
"""

PORT = 2694  # The port used for the socket
HOST_SERVER = None
using_udp = None

# Get command line options
try:
    opts, args = getopt.getopt(sys.argv[1:], "s:p:")
except getopt.GetoptError:
    print "Usage: client.py -s <host> -p <udp | tcp>"
    sys.exit(2)

# If there are no command line options, prompt for a host and use TCP.
if len(opts) == 0:
    HOST_SERVER = raw_input("Enter the host server address: ")
    using_udp = False

# Look through the command line options
for opt, arg in opts:
    if opt == '-s':
        HOST_SERVER = arg
    elif opt == '-p':
        if arg == 'udp':
            using_udp = True
        elif arg == 'tcp':
            using_udp = False
        else:
            print "Option invalid. Please use 'udp' or 'tcp' as an option."
            sys.exit(2)

# If no host server specified, ask for one
if HOST_SERVER is None:
    HOST_SERVER = raw_input("Enter the host server address: ")

# If protocol is unspecified, use TCP.
if using_udp is None:
    using_udp = False


print "Using host " + str(HOST_SERVER)
print "Using UDP..." if using_udp else "Using TCP..."


host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Sending Latency Test: 1 byte"
lat1_tx_time = send_latency(1, host_socket)
lat1_rx_time = receive_latency(1, host_socket)
lat1_rtt_time = lat1_rx_time - lat1_tx_time
print "Latency 1 byte result: " + str(lat1_rtt_time * 1000)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Sending Latency Test: 32 bytes"
lat32_tx_time = send_latency(32, host_socket)
lat32_rx_time = receive_latency(32, host_socket)
lat32_rtt_time = lat32_rx_time - lat32_tx_time
print "Latency 32 byte result: " + str(lat32_rtt_time * 1000)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Sending Latency Test: 1024 bytes"
lat1024_tx_time = send_latency(1024, host_socket)
lat1024_rx_time = receive_latency(1024, host_socket)
lat1024_rtt_time = lat1024_rx_time - lat1024_tx_time
print "Latency 1024 byte result: " + str(lat1024_rtt_time * 1000)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 1 KBytes"
tp1k_tx_rate = calc_throughput(1000, host_socket)
print "Throughput 1 Kbyte result: " + str(tp1k_tx_rate)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 16 KBytes"
tp16k_tx_rate = calc_throughput(16000, host_socket)
print "Throughput 16 Kbyte result: " + str(tp16k_tx_rate)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 64 KBytes"
tp64k_tx_rate = calc_throughput(64000, host_socket)
print "Throughput 64 Kbyte result: " + str(tp64k_tx_rate)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 256 KBytes"
tp256k_tx_rate = calc_throughput(256000, host_socket)
print "Throughput 256 Kbyte result: " + str(tp256k_tx_rate)

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 1 MBytes"
tp1m_tx_rate = calc_throughput(1000000, host_socket)
print "Throughput 1 Mbyte result: " + str(tp1m_tx_rate)


# Close the connection
host_socket.close()



