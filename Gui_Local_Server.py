import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

LOCAL_SERVER_PORT = 9090

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

class LocalServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Server")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)
        self.text_area.insert(tk.END, "Local Server listening on port 9090...\n")

        self.entry = tk.Entry(root, width=40)
        self.entry.grid(column=0, row=1, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_response)
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', LOCAL_SERVER_PORT))
        self.server_socket.listen(5)

        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            self.client_socket, addr = self.server_socket.accept()
            self.text_area.insert(tk.END, f"Connection established with {addr}\n")
            threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                encrypted_data = self.client_socket.recv(1024)
                if encrypted_data:
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    message = caesar_decrypt(decrypted_data.decode())
                    self.text_area.insert(tk.END, f"VPN Server: {message}\n")
                    if message.lower() == "bye":
                        self.text_area.insert(tk.END, "Ending conversation.\n")
                        break
            except Exception as e:
                self.text_area.insert(tk.END, f"Error: {e}\n")
                break

    def send_response(self, event=None):
        response = self.entry.get()
        self.text_area.insert(tk.END, f"Local Server: {response}\n")
        caesar_encrypted = caesar_encrypt(response)
        final_encrypted = cipher_suite.encrypt(caesar_encrypted.encode())
        self.client_socket.send(final_encrypted)
        
        self.entry.delete(0, tk.END)

root = tk.Tk()
app = LocalServerApp(root)
root.mainloop()
