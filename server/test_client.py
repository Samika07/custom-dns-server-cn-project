import socket

SERVER_IP = "127.0.0.1"
PORT = 8053

# Ask user for domain
domain = input("Enter domain: ")

# Build DNS query packet
packet = b'\xaa\xaa'          # Transaction ID
packet += b'\x01\x00'         # Standard query
packet += b'\x00\x01'         # Questions = 1
packet += b'\x00\x00'         # Answer RRs
packet += b'\x00\x00'         # Authority RRs
packet += b'\x00\x00'         # Additional RRs

# Convert domain to DNS format
for part in domain.split("."):
    packet += bytes([len(part)])
    packet += part.encode()

packet += b'\x00'             # End of domain name
packet += b'\x00\x01'         # Type A
packet += b'\x00\x01'         # Class IN

# Send packet
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(packet, (SERVER_IP, PORT))

# Receive response
data, _ = sock.recvfrom(512)

print("Response received from DNS server")
sock.close()
