import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        return

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    try:
     
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))

            
            request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
            client_socket.sendall(request.encode())

            
            response = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data

            print("[RESPONS DARI SERVER]")
            print(response.decode(errors="ignore"))

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()