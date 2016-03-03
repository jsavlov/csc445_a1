import socket
import time
from socket_helper import send_udp_friendly, udp_message_size

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

    s_time = time.time()
    amount_sent = 0

    if s_lat_sock.type is socket.SOCK_DGRAM and len(lat_array) > udp_message_size:
        send_udp_friendly(lat_array, s_lat_sock)
    else:
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

    r_time = time.time()
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

    s_time_b = time.time()
    amount_sent = 0

    if tp_sock.type is socket.SOCK_DGRAM and len(tp_array) > udp_message_size:
        send_udp_friendly(tp_array, tp_sock)
    else:
        while amount_sent < len(tp_array):
            sent = tp_sock.send(tp_array[amount_sent:])
            amount_sent += sent

    tp_sock.shutdown(socket.SHUT_RD)
    s_time_e = time.time()
    s_time = s_time_e - s_time_b

    reply_bytes = []

    r_time_b = time.time()
    data = tp_sock.recv(4096)
    while data != '':
        reply_bytes.append(data)
        data = tp_sock.recv(4096)

    tp_sock.close()
    r_time_e = time.time()
    r_time = r_time_e - r_time_b

    tx_time = (r_time + s_time) / 2

    tx_rate = tp_size / tx_time

    return tx_rate

def observe_interaction(m_size, m_parts, i_sock):
    b_array = bytearray()
    i = 0

    b_array.append(3)
    i += 1
    while i < m_size - 1:
        b_array.append(0)
        i += 1

    b_array.append(255)
    i += 1

    start_time = time.time()

    parts_sent = 0
    while parts_sent < m_parts:
        amount_sent = 0
        while amount_sent < len(b_array):
            sent = i_sock.send(b_array[amount_sent:])
            amount_sent += sent

        reply_found = False
        while reply_found is False:
            reply_conf = i_sock.recv(32)
            response = bytearray(reply_conf)
            if len(reply_conf) > 0 and int(reply_conf) == 3:
                parts_sent += 1
                reply_found = True

    i_sock.close()
    end_time = time.time()
    return end_time - start_time



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

    if sock.type is socket.SOCK_DGRAM and len(lat_reply) > udp_message_size:
        send_udp_friendly(lat_reply, sock)
    else:
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

    if tp_sock.type is socket.SOCK_DGRAM and len(tp_reply) > udp_message_size:
        send_udp_friendly(tp_reply, tp_sock)
    else:
        while amount_sent < len(tp_reply):
            sent = tp_sock.send(tp_reply[amount_sent:])
            amount_sent += sent
            print "** Sent " + str(sent) + " of " + str(len(tp_reply)) + "..."

    print "Throughput reply sent..."

def test_interaction(i_sock):
    i_sock.send(bytearray(bytes(3)))

    inc_data = i_sock.recv(4096)
    while inc_data != '':
        inc_data_len = len(inc_data)
        if ord(inc_data[inc_data_len - 1]) == 255:
            i_sock.send(bytearray(bytes(3)))
        inc_data = i_sock.recv(4096)

    print "Done testing interaction"