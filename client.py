# CSC 445 - Assignment 1
# client.py

import sys
import getopt
from socket_helper import fresh_client_socket
from socket_functions import send_latency, receive_latency, calc_throughput, observe_interaction


PORT = 2694  # The port used for the socket
HOST_SERVER = None
using_udp = None

# A usage message to help users who are unfamiliar with the program

usage = "Usage: client.py -s <host> -p <udp | tcp>"

# Get command line options
try:
    opts, args = getopt.getopt(sys.argv[1:], "s:p:")
except getopt.GetoptError:
    print str(usage)
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
            print str(usage)
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
print "Latency 1 byte result: " + str(float("%.5f" % (lat1_rtt_time * 1000))) + " ms"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Sending Latency Test: 32 bytes"
lat32_tx_time = send_latency(32, host_socket)
lat32_rx_time = receive_latency(32, host_socket)
lat32_rtt_time = lat32_rx_time - lat32_tx_time
print "Latency 32 byte result: " + str(float("%.5f" % (lat32_rtt_time * 1000))) + " ms"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Sending Latency Test: 1024 bytes"
lat1024_tx_time = send_latency(1024, host_socket)
lat1024_rx_time = receive_latency(1024, host_socket)
lat1024_rtt_time = lat1024_rx_time - lat1024_tx_time
print "Latency 1024 byte result: " + str(float("%.5f" % (lat1024_rtt_time * 1000))) + " ms"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 1 KBytes"
tp1k_tx_rate = calc_throughput(1000, host_socket)
print "Throughput 1 Kbyte result: " + str(float("%.5f" % (tp1k_tx_rate / 1000000))) + " MB/s"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 16 KBytes"
tp16k_tx_rate = calc_throughput(16000, host_socket)
print "Throughput 16 Kbyte result: " + str(float("%.5f" % (tp16k_tx_rate / 1000000))) + " MB/s"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 64 KBytes"
tp64k_tx_rate = calc_throughput(64000, host_socket)
print "Throughput 64 Kbyte result: " + str(float("%.5f" % (tp64k_tx_rate / 1000000))) + " MB/s"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 256 KBytes"
tp256k_tx_rate = calc_throughput(256000, host_socket)
print "Throughput 256 Kbyte result: " + str(float("%.5f" % (tp256k_tx_rate / 1000000))) + " MB/s"

host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
print "Throughput test: 1 MBytes"
tp1m_tx_rate = calc_throughput(1000000, host_socket)
print "Throughput 1 Mbyte result: " + str(float("%.5f" % (tp1m_tx_rate / 1000000))) + " MB/s"

# If we aren't using UDP, do the interaction tests
if using_udp is False:
    host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
    print "Interaction test: 256 x 4KByte messages"
    interaction_4kb_time = observe_interaction(4096, 256, host_socket)
    print "Interaction test 256 x 4KByte result: " + str(float("%.5f" % interaction_4kb_time)) + " sec"

    host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
    print "Interaction test: 512 x 2KByte messages"
    interaction_2kb_time = observe_interaction(2048, 512, host_socket)
    print "Interaction test 512 x 2KByte result: " + str(float("%.5f" % interaction_2kb_time)) + " sec"

    host_socket = fresh_client_socket(HOST_SERVER, PORT, using_udp)
    print "Interaction test: 1024 x 1KByte messages"
    interaction_1kb_time = observe_interaction(1024, 1024, host_socket)
    print "Interaction test 1024 x 1KByte result: " + str(float("%.5f" % interaction_1kb_time)) + " sec"

# Close the connection
host_socket.close()



