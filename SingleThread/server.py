import socket
import os

HOST = '0.0.0.0'
PORT = 6789

def handle_client(client_socket, client_address):
    try:
        print(f"[+] Koneksi dari {client_address}")

        request = client_socket.recv(1024).decode()
        print(f"[REQUEST] {request}")

        lines = request.splitlines()
        if len(lines) > 0:
            method, path, _ = lines[0].split()
            filename = path.lstrip('/')

            if method != 'GET':
                response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"
                client_socket.sendall(response.encode())
            elif not os.path.isfile(filename):
                response = "HTTP/1.1 404 Not Found\r\n\r\n404 File Not Found"
                client_socket.sendall(response.encode())
            else:
                with open(filename, 'rb') as f:
                    content = f.read()

                header = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                ).encode()

                client_socket.sendall(header + content)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print(f"[-] Koneksi ditutup dari {client_address}")

def main():
    print("[*] Server SINGLE THREAD sedang berjalan")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[*] Listening di {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()
