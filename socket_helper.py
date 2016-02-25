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