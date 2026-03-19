import socket
from concurrent.futures import ThreadPoolExecutor
from dns_parser import parse_dns_query

PORT = 8053
BUFFER_SIZE = 512


def load_dns_records():
    records = {}
    with open("dns_records.txt") as f:
        for line in f:
            domain, ip = line.strip().split()
            records[domain] = ip
    return records


def build_response(query):
    """
    Build simple DNS response (echo packet for now)
    """
    transaction_id = query[:2]
    flags = b'\x81\x80'
    qdcount = b'\x00\x01'
    ancount = b'\x00\x01'
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'

    header = transaction_id + flags + qdcount + ancount + nscount + arcount

    return header + query[12:]


def handle_request(data, addr, sock, dns_records):
    try:
        # Basic packet validation
        if not data:
            print("Empty packet received")
            return

        if len(data) < 12:
            print("Malformed DNS packet (too short)")
            return

        if len(data) > BUFFER_SIZE:
            print("Oversized packet detected")
            return

        # Safe parsing
        try:
            domain = parse_dns_query(data)
        except Exception:
            print("Failed to parse DNS query")
            return

        # Domain validation
        if not domain or len(domain) > 253:
            print("Invalid domain format")
            return

        print("\nReceived Query:", domain)

        # Safe lookup
        if domain in dns_records:
            print("Resolved locally →", dns_records[domain])
        else:
            print("Domain not in local database")

        # Safe response creation
        try:
            response = build_response(data)
        except Exception:
            print("Failed to build response")
            return

        sock.sendto(response, addr)

    except Exception as e:
        print("Unexpected error:", e)


def main():
    dns_records = load_dns_records()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORT))

    print(f"DNS Server running on port {PORT}")

    #Thread pool for concurrency
    executor = ThreadPoolExecutor(max_workers=50)

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        executor.submit(handle_request, data, addr, sock, dns_records)


if __name__ == "__main__":
    main()
