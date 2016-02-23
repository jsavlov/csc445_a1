import socket

def fresh_socket(host, port, isUDP=False):
    # The socket object used to connect to the server.
    # If the isUDP parameter of the function is true, socket.SOCK_DGRAM is used.
    # Otherwise, it uses socket.SOCK_STREAM.
    # For more info, see http://www.binarytides.com/programming-udp-sockets-in-python/
    f_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if isUDP else socket.SOCK_STREAM)

    print "Opening connection to host " + str(host) + " on port " + str(port) + "..."

    # Open the connection
    f_socket.connect((host, port))

    print "Connection opened."

    return f_socket
