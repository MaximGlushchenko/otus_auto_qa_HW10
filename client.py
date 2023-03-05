import socket


def send_request(host: str, port: int, request: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(1024).decode()
        return response


if __name__ == "__main__":
    host = "localhost"
    port = 8000

    request = "GET / HTTP/1.1\r\n"
    response = send_request(host, port, request)
    print(response)

    request = "GET /?status=401 HTTP/1.1\r\n header-name-1: test-value-1\r\n\r\n header-name-2: test-value-2\r\n\r\n"
    response = send_request(host, port, request)
    print(response)

    request = "GET /?status=404 HTTP/1.1\r\n header-name-1: test-value-1\r\n\r\n header-name-2: test-value-2\r\n\r\n"
    response = send_request(host, port, request)
    print(response)

    request = "GET /?status=500 HTTP/1.1\r\n header-name-1: test-value-1\r\n\r\n header-name-2: test-value-2\r\n\r\n"
    response = send_request(host, port, request)
    print(response)

    request = "GET /?status=invalid HTTP/1.1\r\n header-name-1: test-value-1\r\n\r\n header-name-2: test-value-2\r\n\r\n"
    response = send_request(host, port, request)
    print(response)
