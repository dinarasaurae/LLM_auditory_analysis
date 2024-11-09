from cryptography.fernet import Fernet

# Генерация ключа
key = Fernet.generate_key()
cipher = Fernet(key)

# Ваш пароль
password = "Simply1@".encode()  # Замените your_password_here на ваш пароль

# Шифрование пароля
encrypted_password = cipher.encrypt(password)

print("Ключ шифрования:", key.decode())
print("Зашифрованный пароль:", encrypted_password.decode())
