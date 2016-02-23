import socket

def fresh_socket(host, port):
    f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # The socket object used to connect to the server

    print "Opening connection to host " + str(host) + " on port " + str(port) + "..."

    # Open the connection
    f_socket.connect((host, port))

    print "Connection opened."

    return f_socket
