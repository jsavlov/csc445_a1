import socket
import time

"""
Client Functions
"""
# Sends latency test to the server
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

# receives the message back from the server
def receive_latency(r_lat_len, r_lat_sock):
    received_bytes = []

    data = r_lat_sock.recv(r_lat_len)
    while data != '':
        received_bytes.append(bytes(data))
        data = r_lat_sock.recv(r_lat_len)

    r_time = time.clock()
    r_lat_sock.close()
    return r_time

# calculates throughput in the client
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

    tx_rate = (tp_size / 1000) / tx_time

    return tx_rate

"""
Server functions
"""

# Latency logic on the server end
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

# throughput logic on the server end
def test_throughput(tp_data, tp_sock):
    # Send the data back...
    print "Sending throughput reply..."

    data_len = len(tp_data)
    tp_reply = bytearray()

    i = 0

    tp_reply.append(2)

    if data_len != 1:
        i += 1
        while i < data_len - 1:
            tp_reply.append(0)
            i += 1

        tp_reply.append(255)
        i += 1

    amount_sent = 0
    while amount_sent < len(tp_reply):
        sent = tp_sock.send(tp_reply[amount_sent:])
        amount_sent += sent
        print "** Sent " + str(sent) + " of " + str(len(tp_reply)) + "..."

    tp_sock.close()
    print "Throughput reply sent..."