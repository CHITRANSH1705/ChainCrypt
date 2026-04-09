ChainCrypt is a secure file storage system that encrypts and splits files into multiple chunks, stores their integrity using a lightweight blockchain, and sends email notifications upon successful decryption. It uses password-based encryption, GUI interaction, and ensures that the data remains private and tamper-proof.

 🚀 Tech Stack
- Python
- Cryptography (Fernet) for encryption
- JSON (to simulate blockchain)
- smtplib & MIME (for email notifications)

🎯 Features
-  Password-Based Encryption 
  User sets a custom password to encrypt files securely.
-  File Chunking
  Files are split into multiple encrypted chunks (1 MB each).
-  Blockchain Simulation
  Each encrypted chunk is recorded in a local blockchain (JSON) for integrity.
-  Email Notification*
  After successful decryption, a confirmation email is sent to the user.

 🧭 How to Use

 1. Install Dependencies
    pip install cryptography
2. Run the Application
    python gui.py
3. Encrypt a File
4. Select the file you want to encrypt.

Set a password (this will be used to decrypt the file later).

The file is split into chunks and encrypted.

A blockchain.json file is created to track chunk order.

5. Decrypt a File

Enter the same password used during encryption.

Provide an output filename (e.g., Resume_decrypted.pdf).

Enter your email address to receive a confirmation.

The system decrypts and reconstructs the original file.

You receive an email notification on successful decryption.
