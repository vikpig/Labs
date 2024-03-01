import socket
import sys

def send_file(host, port, filename):
    with open(filename, 'r') as f:
        file_content = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(file_content.encode())
        print("File sent successfully")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <filename>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    send_file(host, port, filename)

