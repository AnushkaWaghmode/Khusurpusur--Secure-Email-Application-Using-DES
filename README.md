# Secure Email Application using DES

A beginner-friendly Network Security mini-project built using:

- Python
- Tkinter
- Python socket programming
- DES encryption/decryption

## 1. What does this project do?

Two users can open the SecureMail client and exchange email-shaped messages
through a relay server. The interface includes sender, recipient, subject,
and message fields while preserving the original DES demonstration.

Before a message is sent:

    Email plaintext (sender, recipient, subject, body)
        ↓
    DES Encryption
        ↓
    Ciphertext
        ↓
    Socket / Server
        ↓
    Receiver
        ↓
    DES Decryption
        ↓
    Email plaintext in the inbox

The server only forwards the encrypted message. It does not need to know
the original message.

## 2. Project files

### `des.py`
Contains the DES algorithm.

Main functions:

- `encrypt(message, key)` → plaintext to ciphertext
- `decrypt(ciphertext, key)` → ciphertext to plaintext

The DES key used by the GUI is exactly 8 characters.

### `server.py`
Creates the TCP email relay.

Its job is simple:

1. Wait for clients.
2. Accept mailbox connections.
3. Receive encrypted data.
4. Forward encrypted email data to other clients.

The server does NOT decrypt the message.

### `client.py`
Creates the Tkinter SecureMail interface and handles:

- connecting to the server
- entering the DES key
- composing sender, recipient, subject, and message body
- DES encryption
- sending ciphertext
- receiving ciphertext
- DES decryption
- displaying received emails and the encryption/decryption audit trail

## 3. Requirements

Python 3.x is enough.

Tkinter is normally included with standard Python installations.

No external package is required.

## 4. How to run

Open Terminal 1:

    python server.py

Then open Terminal 2 for client 1:

    python client.py 1

Then open Terminal 3 for client 2:

    python client.py 2

The clients use these example email identities:

    client1@khusurpusur.com
    client2@khusurpusur.com

To run more clients, use their number as the argument, for example:

    python client.py 3

This creates `client3@khusurpusur.com`. Type the intended client email in the
`To` field. After decryption, each mailbox displays the email only when the
`To` address matches its own email ID; other clients ignore it.

Use the SAME 8-character DES key in both clients, for example:

    SECURE12

Fill in the email fields and press `Encrypt and Send`.

## 5. Important

Start `server.py` first.

Then start at least two copies of `client.py`.

For the same computer, `127.0.0.1` is used.

For two computers on the same LAN, change `SERVER_HOST` in `client.py`
to the IP address of the computer running `server.py`.

Example:

    SERVER_HOST = "192.168.1.10"

The firewall may need to allow Python on port 5000.

## 6. Why does this match Network Security?

This project demonstrates:

- Encryption
- Decryption
- Symmetric key cryptography
- DES
- Plaintext
- Ciphertext
- Secret key
- Socket programming
- Secure message transmission concept

## 7. Viva explanation in 30 seconds

"Our project is a secure email demonstration. We used Python, Tkinter and TCP
socket programming. When a user sends an email, its sender, recipient,
subject and body are encrypted locally using DES and converted into
ciphertext. The relay only forwards that ciphertext. The recipient uses the
same secret DES key to decrypt it and recover the email. Thus the project
demonstrates encryption, decryption and symmetric-key cryptography through an
email-style interface."

## 8. Important security limitation

This is an academic demonstration of DES and socket programming.

DES is an old cipher and is not considered secure for modern real-world
applications. Do not present this project as production-grade security.

For the college mini-project, the purpose is to demonstrate the NSC concepts
clearly.
