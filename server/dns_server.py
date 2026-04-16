import socket
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


def main():
    dns_records = load_dns_records()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 8053))

    print(f"DNS Server running on port {PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)

        domain = parse_dns_query(data)

        print("\nReceived Query:", domain)

        if domain in dns_records:
            print("Resolved locally →", dns_records[domain])
        else:
            print("Domain not in local database")

        response = build_response(data)

        sock.sendto(response, addr)


if __name__ == "__main__":
    main()
