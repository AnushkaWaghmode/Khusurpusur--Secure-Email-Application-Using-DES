import socket
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from des import encrypt, decrypt

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
CLIENT_EMAIL_DOMAIN = "khusurpusur.com"


def client_email(client_number):
    return f"client{client_number}@{CLIENT_EMAIL_DOMAIN}"


def is_client_email(address):
    local_part, separator, domain = address.lower().partition("@")
    client_number = local_part[6:]
    return (
        bool(separator)
        and domain == CLIENT_EMAIL_DOMAIN
        and local_part.startswith("client")
        and client_number.isdigit()
        and int(client_number) > 0
    )


class SecureChatClient:
    def __init__(self, root, client_number=1):
        self.root = root
        self.client_number = client_number
        self.client_email = client_email(client_number)
        self.root.title("SecureMail - DES Encrypted Email")
        self.root.geometry("760x700")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.socket = None
        self.connected = False

        title = tk.Label(
            root,
            text="Khusurpusur",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(10, 3))

        subtitle = tk.Label(
            root,
            text="Secure Email for all your GOSSIPS :)",
            font=("Arial", 10)
        )
        subtitle.pack()

        security = tk.LabelFrame(root, text="Security", padx=8, pady=8)
        security.pack(fill="x", padx=12, pady=12)

        tk.Label(security, text="DES key (8 characters):").grid(
            row=0, column=0, padx=5
        )

        self.key_entry = tk.Entry(security, width=14, show="*")
        self.key_entry.insert(0, "SECURE12")
        self.key_entry.grid(row=0, column=1, padx=5, sticky="w")

        self.connect_button = tk.Button(
            security, text="Open Mailbox", width=14, command=self.connect
        )
        self.connect_button.grid(row=0, column=2, padx=5)

        self.status = tk.Label(root, text="Mailbox offline", fg="red")
        self.status.pack()

        inbox = tk.LabelFrame(root, text="Inbox / Encryption Audit", padx=8, pady=8)
        inbox.pack(fill="both", expand=True, padx=12, pady=(8, 6))

        self.chat_box = scrolledtext.ScrolledText(
            inbox, width=82, height=15, state="disabled", wrap="word"
        )
        self.chat_box.pack(fill="both", expand=True)

        compose = tk.LabelFrame(root, text="Compose Secure Email", padx=8, pady=8)
        compose.pack(fill="x", padx=12, pady=6)

        tk.Label(compose, text="From:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.sender_entry = tk.Entry(compose, width=28, state="readonly")
        self.sender_entry.config(state="normal")
        self.sender_entry.insert(0, self.client_email)
        self.sender_entry.config(state="readonly")
        self.sender_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=3)

        tk.Label(compose, text="To:").grid(row=0, column=2, sticky="w", padx=4, pady=3)
        self.recipient_entry = tk.Entry(compose, width=28)
        self.recipient_entry.insert(0, "recipient@securemail.local")
        self.recipient_entry.grid(row=0, column=3, sticky="ew", padx=4, pady=3)

        tk.Label(compose, text="Subject:").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.subject_entry = tk.Entry(compose)
        self.subject_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=4, pady=3)

        self.message_entry = scrolledtext.ScrolledText(compose, height=4, wrap="word")
        self.message_entry.grid(row=2, column=0, columnspan=4, sticky="ew", padx=4, pady=4)

        self.send_button = tk.Button(
            compose, text="Encrypt and Send", width=18, command=self.send_message
        )
        self.send_button.grid(row=3, column=3, sticky="e", padx=4, pady=4)
        compose.columnconfigure(1, weight=1)
        compose.columnconfigure(3, weight=1)

        note = tk.Label(
            root,
            text="Academic demo only: DES is obsolete for real-world security.",
            font=("Arial", 9)
        )
        note.pack(pady=5)

        self.root.after(200, self.sender_entry.focus)

    def add_chat(self, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", text + "\n")
        self.chat_box.see("end")
        self.chat_box.config(state="disabled")

    def connect(self):
        if self.connected:
            return

        key = self.key_entry.get()
        if len(key) != 8:
            messagebox.showerror(
                "Invalid Key",
                "DES key must contain exactly 8 characters."
            )
            return

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True

            self.status.config(text="Mailbox online - encrypted channel ready", fg="green")
            self.connect_button.config(state="disabled")
            self.add_chat("[MAILBOX] Connected. Emails are encrypted before transmission.")

            thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )
            thread.start()

        except OSError as error:
            messagebox.showerror(
                "Connection Error",
                f"Could not connect to server.\n\n{error}\n\n"
                "Make sure server.py is running first."
            )
            if self.socket:
                self.socket.close()
                self.socket = None

    def send_message(self):
        if not self.connected:
            messagebox.showwarning("Not Connected", "Connect to the server first.")
            return

        sender = self.sender_entry.get().strip()
        recipient = self.recipient_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_entry.get("1.0", "end-1c").strip()
        key = self.key_entry.get()

        if not sender or not recipient or not subject or not message:
            messagebox.showwarning(
                "Incomplete Email",
                "From, To, Subject, and Message are required."
            )
            return

        if not is_client_email(recipient):
            messagebox.showwarning(
                "Invalid Recipient",
                "Use a client email such as client3@khusurpusur.com."
            )
            return

        try:
            email = (
                f"From: {sender}\n"
                f"To: {recipient}\n"
                f"Subject: {subject}\n\n"
                f"{message}"
            )

            # Encryption happens BEFORE the email enters the network.
            ciphertext = encrypt(email, key)

            # Simple protocol: send only ciphertext.
            packet = (ciphertext + "\n").encode("ascii")
            self.socket.sendall(packet)

            self.add_chat(f"[SENT] To: {recipient} | Subject: {subject}")
            self.add_chat(f"[ENCRYPTED] Ciphertext sent through relay: {ciphertext}")
            self.subject_entry.delete(0, "end")
            self.message_entry.delete("1.0", "end")

        except Exception as error:
            messagebox.showerror("Encryption Error", str(error))

    def receive_messages(self):
        buffer = ""

        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break

                buffer += data.decode("ascii")

                # Each message ends with newline.
                while "\n" in buffer:
                    ciphertext, buffer = buffer.split("\n", 1)

                    if not ciphertext:
                        continue

                    try:
                        email = decrypt(
                            ciphertext,
                            self.key_entry.get()
                        )
                        headers, body = email.split("\n\n", 1)
                        fields = {}
                        for line in headers.splitlines():
                            label, value = line.split(": ", 1)
                            fields[label] = value
                        if fields.get("To", "").strip().lower() != self.client_email.lower():
                            continue
                        self.root.after(
                            0,
                            self.add_chat,
                            f"[RECEIVED] From: {fields['From']} | "
                            f"Subject: {fields['Subject']}\n{body}"
                        )
                        self.root.after(
                            0,
                            self.add_chat,
                            f"[DECRYPTED] Ciphertext received and opened: {ciphertext}"
                        )
                    except Exception:
                        self.root.after(
                            0,
                            self.add_chat,
                            "[ERROR] Could not decrypt email. "
                            "Check that both users use the same 8-character key."
                        )

            except (OSError, ConnectionResetError):
                break

        if self.connected:
            self.connected = False
            self.root.after(
                0,
                lambda: self.status.config(
                    text="Mailbox offline", fg="red"
                )
            )

    def close(self):
        self.connected = False
        try:
            if self.socket:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
        except OSError:
            pass
        self.root.destroy()


if __name__ == "__main__":
    try:
        client_number = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        if client_number < 1:
            raise ValueError
    except ValueError:
        raise SystemExit("Usage: python client.py [client number]")

    root = tk.Tk()
    app = SecureChatClient(root, client_number)
    root.mainloop()
