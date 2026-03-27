import socket
import json

PORT = 8054

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("[ROOT DNS] Running...")

while True:
    data, addr = sock.recvfrom(512)
    query = json.loads(data.decode())

    domain = query["domain"]
    print("[ROOT DNS] Query:", domain)

    
    response = {
        "next": "TLD",
        "ip": "192.168.1.5",   
        "port": 8055
    }

    sock.sendto(json.dumps(response).encode(), addr)
