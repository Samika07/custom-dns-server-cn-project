import socket
import json

PORT = 8056

DNS_RECORDS = {
    "www.google.com": "142.250.190.78",
    "example.com": "93.184.216.34"
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("[AUTH DNS] Running...")

while True:
    data, addr = sock.recvfrom(512)
    query = json.loads(data.decode())

    domain = query["domain"]
    qtype = query.get("type", "A")

    print("[AUTH DNS] Query:", domain)

    ip = DNS_RECORDS.get(domain, "0.0.0.0")

    response = {
        "domain": domain,
        "type": qtype,
        "ip": ip
    }

    sock.sendto(json.dumps(response).encode(), addr)
