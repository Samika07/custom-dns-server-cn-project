import struct

def parse_dns_query(data):
    """
    Extract domain name from DNS query packet
    """
    domain = []
    i = 12   # DNS header size

    length = data[i]

    while length != 0:
        i += 1
        domain.append(data[i:i+length].decode())
        i += length
        length = data[i]

    domain_name = ".".join(domain)
    return domain_name
