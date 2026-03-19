import socket
import threading
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8053
BUFFER_SIZE = 512

DNS_QUERY = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'


def send_request(results, index):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(2)

        start = time.time()
        client.sendto(DNS_QUERY, (SERVER_IP, SERVER_PORT))
        client.recvfrom(BUFFER_SIZE)
        end = time.time()

        results[index] = end - start

    except Exception:
        results[index] = None


def run_test(num_requests):
    threads = []
    results = [0] * num_requests

    start_time = time.time()

    for i in range(num_requests):
        t = threading.Thread(target=send_request, args=(results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    valid_times = [r for r in results if r is not None]

    print(f"\n--- Test with {num_requests} concurrent requests ---")
    print(f"Total time: {end_time - start_time:.4f} seconds")

    if valid_times:
        print(f"Average response time: {sum(valid_times)/len(valid_times):.4f} seconds")
        print(f"Successful responses: {len(valid_times)}/{num_requests}")
    else:
        print("No successful responses")


if __name__ == "__main__":
    for n in [10, 50, 100, 200]:
        run_test(n)
