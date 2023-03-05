import socket
import http
from urllib.parse import parse_qsl


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode()
    print(f"Request data: {request_data}")

    request_line, headers = request_data.split('\r\n', 1)
    request_method, path, _ = request_line.split(' ')
    print(f"Request method: {request_method}")
    print(f"Path: {path}")

    status_code = 200
    query_string = path.split('?', 1)[-1]
    query_params = dict(parse_qsl(query_string))
    if 'status' in query_params:
        try:
            status_code = int(query_params['status'])
        except ValueError:
            pass

    response_status = f"{status_code} {http.HTTPStatus(status_code).phrase}"
    response_headers = [
        f"Request Method: {request_method}",
        f"Request Source: {client_socket.getpeername()}",
        f"Response Status: {response_status}"
    ]
    for header_line in headers.split('\r\n'):
        if header_line:
            response_headers.append(header_line)
    response_headers.append('')
    response_data = '\r\n'.join(response_headers)
    client_socket.sendall(response_data.encode())

    client_socket.close()


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ("localhost", 8000)
    server_socket.bind(server_address)

    server_socket.listen()

    print(f"Ожидание запроса на {server_address}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Установлено соединение с {client_address}")

        handle_request(client_socket)


if __name__ == "__main__":
    run_server()
