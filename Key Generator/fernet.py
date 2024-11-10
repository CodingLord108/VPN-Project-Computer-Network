from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Fernet Key: {key.decode()}")
