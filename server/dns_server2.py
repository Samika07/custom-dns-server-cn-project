import socket
import json
from concurrent.futures import ThreadPoolExecutor
from dns_parser import parse_dns_query

PORT = 8053
BUFFER_SIZE = 512


def send_query(ip, port, query):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(query).encode(), (ip, port))
    data, _ = sock.recvfrom(512)
    return json.loads(data.decode())


def load_dns_records():
    records = {}
    with open("dns_records.txt") as f:
        for line in f:
            domain, ip = line.strip().split()
            records[domain] = ip
    return records


def handle_request(data, addr, sock, dns_records):
    try:
        
        if not data:
            print("Empty packet received")
            return

        if len(data) < 12:
            print("Malformed DNS packet (too short)")
            return

        if len(data) > BUFFER_SIZE:
            print("Oversized packet detected")
            return

        # ---------------- PARSE DOMAIN ----------------
        try:
            domain = parse_dns_query(data)
        except Exception:
            print("Failed to parse DNS query")
            return

        if not domain or len(domain) > 253:
            print("Invalid domain format")
            return

        print("\n[LOCAL DNS] Received:", domain)

        # ---------------- QUERY OBJECT ----------------
        query = {
            "domain": domain,
            "type": "A",
            "mode": "recursive"
        }

        # ---------------- LOCAL LOOKUP ----------------
        if domain in dns_records:
            print("[LOCAL DNS] Resolved locally →", dns_records[domain])

            response = {
                "domain": domain,
                "type": "A",
                "ip": dns_records[domain]
            }

        else:
            print("[LOCAL DNS] Forwarding to ROOT DNS...")

            
            SERVER_IP = "192.168.1.5"

            # Step 1: Root
            root_res = send_query(SERVER_IP, 8054, query)

            # Step 2: TLD
            tld_res = send_query(root_res["ip"], root_res["port"], query)

            # Step 3: AUTH
            auth_res = send_query(tld_res["ip"], tld_res["port"], query)

            response = auth_res

       
        sock.sendto(json.dumps(response).encode(), addr)

    except Exception as e:
        print("Unexpected error:", e)


def main():
    dns_records = load_dns_records()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORT))

    print(f"[LOCAL DNS] Running on port {PORT}")

    executor = ThreadPoolExecutor(max_workers=50)

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        executor.submit(handle_request, data, addr, sock, dns_records)


if __name__ == "__main__":
    main()
