import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet
import logging

# Logging configuration
logging.basicConfig(
    filename="vpn_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

VPN_SERVER_PORT = 8080
LOCAL_SERVER_HOST = '127.0.0.1'
LOCAL_SERVER_PORT = 9090

# Fernet Key
FERNET_KEY = b'VP6obS19cg8bCRukbJGNxWSk_ctFGkjJ13Wh2PlHHxQ='
cipher_suite = Fernet(FERNET_KEY)

def caesar_encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift)

class VPNServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VPN Server")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)
        self.text_area.insert(tk.END, "VPN Server listening on port 8080...\n")
        logging.info("VPN Server started on port 8080")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', VPN_SERVER_PORT))
        self.server_socket.listen(5)

        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.secure_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
            self.text_area.insert(tk.END, f"Connected with {addr}\n")
            logging.info(f"SSL connection established with {addr}")
            threading.Thread(target=self.handle_client, daemon=True).start()

    def handle_client(self):
        while True:
            try:
                encrypted_data = self.secure_socket.recv(1024)
                if encrypted_data:
                    self.text_area.insert(tk.END, f"Encrypted Client Message: {encrypted_data}\n")
                    logging.info(f"Received encrypted message from Client: {encrypted_data}")
                    
                    response = self.forward_to_local_server(encrypted_data)
                    
                    self.text_area.insert(tk.END, f"Encrypted Local Server Response: {response}\n")
                    logging.info(f"Encrypted response from Local Server: {response}")
                    
                    self.secure_socket.send(response)
            except Exception as e:
                logging.error(f"Error handling client: {e}")
                break

    def forward_to_local_server(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as local_socket:
            local_socket.connect((LOCAL_SERVER_HOST, LOCAL_SERVER_PORT))
            local_socket.sendall(data)
            response = local_socket.recv(1024)
            return response

root = tk.Tk()
app = VPNServerApp(root)
root.mainloop()
