import os
import json
import smtplib
import base64
from email.mime.text import MIMEText
from cryptography.fernet import Fernet

# --------- Encryption Utilities --------->
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.encode('utf-8').ljust(32)[:32])
def encrypt_chunks(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)
    blockchain = []
    with open(file_path, "rb") as file:
        chunk_num = 0
        while chunk := file.read(1024 * 1024):  # 1MB per chunk
            encrypted_chunk = fernet.encrypt(chunk)
            chunk_name = f"{os.path.basename(file_path)}.chunk{chunk_num}"
            with open(chunk_name, "wb") as chunk_file:
                chunk_file.write(encrypted_chunk)
            blockchain.append(chunk_name)
            print(f" Encrypted and saved: {chunk_name}")
            chunk_num += 1
    with open("blockchain.json", "w") as f:
        json.dump(blockchain, f)
    print("\n File encrypted and blockchain saved.")

# --------- Decryption Utilities ---------
def decrypt_chunks(output_file, password, user_email):
    key = generate_key(password)
    fernet = Fernet(key)
    if not os.path.exists("blockchain.json"):
        print("Blockchain not found!")
        return

    with open("blockchain.json", "r") as f:
        try:
            blockchain = json.load(f)
        except json.JSONDecodeError:
            print(" Blockchain file is corrupted or empty.")
            return
    with open(output_file, "wb") as output:
        for chunk in blockchain:
            if not os.path.exists(chunk):
                print(f" Missing chunk: {chunk}")
                return
            with open(chunk, "rb") as chunk_file:
                encrypted_data = chunk_file.read()
                try:
                    decrypted_data = fernet.decrypt(encrypted_data)
                    output.write(decrypted_data)
                except Exception:
                    print(" Decryption failed. Invalid password or corrupt chunk.")
                    return
    print(f"\n File reconstructed as {output_file}")
    send_email_notification(user_email, output_file)

# --------- Email Notification ---------
def send_email_notification(receiver_email, filename):
    sender_email = "SET_YOURMAIL@gmail.com"        
    sender_password = "SET_PASSWORD"        
    msg = MIMEText(f"Your file '{filename}' has been successfully decrypted.")
    msg['Subject'] = " File Decryption Complete"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f" Email notification sent to {receiver_email}")
    except Exception as e:
        print(" Failed to send email:", str(e))

# --------- Main Menu ---------
def main():
    print("\n Secure File Storage Using Blockchain and Encryption")
    print("------------------------------------------------------")
    choice = input("1. Encrypt & Store File\n2. Decrypt File\nChoose (1/2): ")
    if choice == "1":
        file_path = input(" Enter path to file: ").strip('"')
        if not os.path.exists(file_path):
            print(" File not found!")
            return
        password = input(" Set a password for encryption: ")
        encrypt_chunks(file_path, password)
    elif choice == "2":
        output_file = input(" Enter output filename (e.g., secret.pdf): ")
        password = input(" Enter your password to decrypt: ")
        user_email = input(" Enter your email to receive notification: ")
        decrypt_chunks(output_file, password, user_email)
    else:
        print(" Invalid choice.")
if __name__ == "__main__":
    main()