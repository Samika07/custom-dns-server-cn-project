def parse_dns_query(data):
    """
    Safely extract domain name from DNS packet
    """

    domain = []
    i = 12   # DNS header starts after 12 bytes

    try:
        while i < len(data):
            length = data[i]

            if length == 0:
                break

            i += 1

            label = data[i:i + length].decode(errors="ignore")
            domain.append(label)

            i += length

        return ".".join(domain)

    except Exception as e:
        print("Parser Error:", e)
        return "invalid.query"
