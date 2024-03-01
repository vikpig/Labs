import socket
import threading
import signal
import sys
import json

class ThreadPool:
    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.pool = []
        self.lock = threading.Lock()

    def acquire(self):
        while True:
            if len(self.pool) >= self.max_threads:
                time.sleep(0.1)
            else:
                self.lock.acquire()
                thread = threading.Thread()
                self.pool.append(thread)
                self.lock.release()
                return thread

    def release(self, thread):
        with self.lock:
            self.pool.remove(thread)


class FileServer:
    def __init__(self, host, port, max_threads, max_file_size, save_path):
        self.host = host
        self.port = port
        self.max_threads = max_threads
        self.max_file_size = max_file_size
        self.save_path = save_path
        self.thread_pool = ThreadPool(max_threads)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, client_socket, address):
        data = client_socket.recv(1024)
        if data:
            file_content = data.decode()
            filename = f"{self.save_path}"
            with open(filename, 'w') as f:
                f.write(file_content)
            print(f"File received from {address} and saved as {filename}")
        client_socket.close()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address}")
            client_thread = self.thread_pool.acquire()
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def stop(self):
        self.server_socket.close()

def sigterm_handler(signum, frame):
    print('Received SIGTERM. Exiting...')
    sys.exit(0)

def sighup_handler(signum, frame):
    print('Received SIGHUP. Restarting server...')
    restart_server()

def stop(self):
    self.server_socket.close()

def restart_server():
    server.stop()
    new_server = FileServer(config['host'], config['port'], config['max_threads'], config['max_file_size'], config['save_path'])
    new_server.start()


if __name__ == "__main__":
    try:
        with open('server_config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Server configuration file not found.")
        sys.exit(1)

    server = FileServer(config['host'], config['port'], config['max_threads'], config['max_file_size'], config['save_path'])
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGHUP, sighup_handler)
    server.start()

