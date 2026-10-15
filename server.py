"""
server.py
---------
Very small TCP email relay.

The server does NOT encrypt or decrypt messages.
Clients encrypt before sending, and decrypt after receiving.
Therefore the server simply relays ciphertext.
"""

import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
lock = threading.Lock()


def broadcast(message, sender_socket):
    """Send the encrypted message to every connected client except sender."""
    with lock:
        for client in clients[:]:
            if client != sender_socket:
                try:
                    client.sendall(message)
                except OSError:
                    remove_client(client)


def remove_client(client_socket):
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
    try:
        client_socket.close()
    except OSError:
        pass


def handle_client(client_socket, address):
    print(f"[+] Client connected: {address}")

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break

        
            broadcast(data, client_socket)

    except ConnectionResetError:
        pass
    finally:
        remove_client(client_socket)
        print(f"[-] Client disconnected: {address}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    print("=" * 55)
    print(" SECURE EMAIL RELAY")
    print("=" * 55)
    print(f"Listening on port {PORT}...")
    print("Start two or more SecureMail clients now.")

    while True:
        client_socket, address = server.accept()

        with lock:
            clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    start_server()
