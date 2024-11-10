import socket
import ssl
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

VPN_SERVER_HOST = '127.0.0.1'
VPN_SERVER_PORT = 8080

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

class VPNClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VPN Client")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.grid(column=0, row=1, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        self.secure_socket = self.context.wrap_socket(self.client_socket, server_hostname=VPN_SERVER_HOST)
        self.secure_socket.connect((VPN_SERVER_HOST, VPN_SERVER_PORT))
        self.text_area.insert(tk.END, "Connected to VPN Server\n")

    def send_message(self, event=None):
        message = self.entry.get()
        self.text_area.insert(tk.END, f"Client: {message}\n")
        
        caesar_encrypted = caesar_encrypt(message)
        final_encrypted = cipher_suite.encrypt(caesar_encrypted.encode())
        self.secure_socket.send(final_encrypted)
        self.entry.delete(0, tk.END)

        data = self.secure_socket.recv(1024)
        if data:
            decrypted_data = cipher_suite.decrypt(data)
            response = caesar_decrypt(decrypted_data.decode())
            self.text_area.insert(tk.END, f"Response from server: {response}\n")

root = tk.Tk()
app = VPNClientApp(root)
root.mainloop()