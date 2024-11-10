# VPN Communication System with Double Encryption

This project demonstrates a simple VPN-like setup with communication between a **VPN Client**, a **VPN Server**, and a **Local Server**, featuring a **Caesar Cipher** and **Fernet** encryption for double-layered security. Each message sent through this system is encrypted first with Caesar Cipher and then with Fernet for enhanced security. The project uses SSL to secure communication between the VPN Client and VPN Server.

## Features

- **Double Encryption**: Messages are first encrypted with Caesar Cipher and then with Fernet.
- **End-to-End Communication**: The system comprises a Client, Server, and Local Server to simulate a VPN setup.
- **Secure SSL**: Communication between VPN Client and VPN Server is secured with SSL.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Generate SSL Certificates](#step-1-generate-ssl-certificates)
  - [Step 2: Generate a Fernet Key](#step-2-generate-a-fernet-key)
  - [Step 3: Update Fernet Key in All Files](#step-3-update-fernet-key-in-all-files)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [File Overview](#file-overview)
- [Encryption Flow](#encryption-flow)

---

## Requirements

- **Python 3.8+**
- **Tkinter** (Usually pre-installed with Python)
- **cryptography** library for Fernet encryption:
  ```bash
  pip install cryptography
  ```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/CodingLord108/VPN-Project-Computer-Network.git
   cd VPN-Project-Computer-Network
   ```

2. Ensure you have all dependencies installed, specifically `cryptography`.

3. Open a terminal in the project directory.

---

## Setup Instructions

### Step 1: Generate SSL Certificates

To secure communication between the VPN Client and VPN Server, generate SSL certificates. In the project root, run the following commands:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server_key.pem -out server_cert.pem -days 365
```

- When prompted, enter a passphrase and certificate information as needed.
- This will generate two files: `server_key.pem` (private key) and `server_cert.pem` (certificate).

### Step 2: Generate a Fernet Key

For message encryption, generate a unique **Fernet key** that will be shared between all components. You can generate the Fernet key by running the following Python code:

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Copy this key for use in the next step
```

### Step 3: Update Fernet Key in All Files

Copy the generated Fernet key and replace the `FERNET_KEY` placeholder in each of the following files:

- `local_server.py`
- `vpn_server.py`
- `vpn_client.py`

Ensure that the same Fernet key is used in all components to maintain the encryption consistency.

---

## Running the Project

Run each component in a separate terminal window or tab, in the following order:

1. **Local Server**:
   ```bash
   python Gui_Local_Server.py
   ```

2. **VPN Server**:
   ```bash
   python Gui_VPN_Server.py
   ```

3. **VPN Client**:
   ```bash
   python Gui_VPN_Client.py
   ```

Each component will open a graphical interface using Tkinter, allowing you to send and receive messages.

---

## Usage

1. **Sending a Message**: In the **VPN Client** window, type a message in the entry box and press Enter. The message will:
   - Be encrypted with Caesar Cipher.
   - Be encrypted with Fernet.
   - Sent securely via SSL to the VPN Server.

2. **Receiving a Message**:
   - The VPN Server will forward the message to the Local Server.
   - The Local Server decrypts the message in reverse order (Fernet decryption followed by Caesar decryption).
   - The response from the Local Server follows the same encryption flow back to the VPN Client.

3. **Exit**: To terminate, type `bye` in the VPN Client, which will signal the end of the conversation and close all connections.

---

## File Overview

- **Gui_Local_Server.py**: Simulates a local server that listens for messages from the VPN Server, decrypts them, processes them, and sends a response.
- **Gui_VPN_Server.py**: Acts as an intermediary server (VPN Server) that handles encrypted communication between the VPN Client and Local Server. Uses SSL and double encryption.
- **Gui_VPN_Client.py**: The client interface that sends encrypted messages to the VPN Server and receives responses.

---

## Encryption Flow

1. **Client Side (VPN Client)**:
   - Message → Caesar Cipher Encryption → Fernet Encryption → SSL Transmission.

2. **Server Side (VPN Server)**:
   - SSL Transmission → Fernet Decryption → Caesar Cipher Decryption → Message Processing (and the reverse for responses).

---

