import socket

def fresh_client_socket(host, port, is_udp=False):
    """
    The socket object used to connect to the server.
    If the is_udp parameter of the function is true, socket.SOCK_DGRAM is used.
    Otherwise, it uses socket.SOCK_STREAM.
    For more info, see http://www.binarytides.com/programming-udp-sockets-in-python/
    """

    f_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if is_udp else socket.SOCK_STREAM)

    print "Opening connection to host " + str(host) + " on port " + str(port) + "..."

    # Open the connection
    f_client_socket.connect((host, port))

    print "Connection opened."

    return f_client_socket

def fresh_server_socket(port, is_udp=False):
    """
    The socket object used as the server.
    If the is_udp parameter of the function is true, socket.SOCK_DGRAM is used.
    Otherwise, it uses socket.SOCK_STREAM.
    For more info, see http://www.binarytides.com/programming-udp-sockets-in-python/
    """

    f_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if is_udp else socket.SOCK_STREAM)

    return f_server_socket

udp_message_size = 8000 # Size of the UDP message in Kilobytes

def send_udp_friendly(data, sock):
    """
    Sometimes you have to send data using UDP. The maximum datagram size is 16KB.
    This function breaks messages up into friendly UDP chunks of appropriate size.
    """

    bytes_sent = 0 # The number of bytes sent
    total_size = len(data) # The total number of bytes

    while bytes_sent < total_size:
        if bytes_sent + udp_message_size > total_size:
            sent = sock.send(data[bytes_sent:total_size])
            bytes_sent += sent
        else:
            sent = sock.send(data[bytes_sent:bytes_sent + udp_message_size])
            bytes_sent += sent
