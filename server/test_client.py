import socket

server = ("127.0.0.1", 8053)

# simple DNS query packet
query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' \
        b'\x06google\x05local\x00\x00\x01\x00\x01'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(query, server)

data, _ = sock.recvfrom(512)

print("Response received from DNS server")