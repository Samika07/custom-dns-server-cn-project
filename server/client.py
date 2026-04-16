import socket
import json

SERVER_IP = "127.0.0.1"  

PORT = 8053

domain = input("Enter domain: ")
mode = input("Enter mode (-i or -r): ")

mode = "iterative" if mode == "-i" else "recursive"

query = {
    "domain": domain,
    "type": "A",
    "mode": mode
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(query).encode(), (SERVER_IP, PORT))

data, _ = sock.recvfrom(512)
print("Response:", json.loads(data.decode()))
