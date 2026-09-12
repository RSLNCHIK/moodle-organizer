import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

MOODLE_TOKEN_KEY = os.getenv("MOODLE_TOKEN_KEY")

if MOODLE_TOKEN_KEY is None:
    raise RuntimeError("Moodle token key is not set.")

# The Fernet class is used to create a symmetric encryption object that can be used to encrypt and decrypt data.
# This is done using the MOODLE_TOKEN_KEY environment variable, which is a secret key used for encryption and decryption. 
# The key is encoded to bytes using the encode() method before being passed to the Fernet constructor.
# We encode the key to bytes because the Fernet class expects a bytes-like object as input for the key. The encode() method converts the string representation of the key into a bytes object, which can then be used for encryption and decryption operations.
fernet = Fernet(MOODLE_TOKEN_KEY.encode())


# the encrypt_token function takes a string token as input, encrypts it using the Fernet object, and returns the encrypted token as a string. 
# The token is first encoded to bytes using the encode() method before being passed to the encrypt() method of the Fernet object.
# encrypted is then decoded back to a string using the decode() method before being returned.
# encrypt and decrypt functions are used to securely store and retrieve sensitive information, such as authentication tokens, in a way that prevents unauthorized access.
# encrypted is a bytes object that represents the encrypted version of the input token. It is returned as a string by decoding it using the decode() method.
# Why give the token as a string and not bytes? Because the token is typically represented as a string in the application, and it is more convenient to work with strings in most cases. By accepting the token as a string, we can easily pass it around in our code without having to worry about encoding and decoding it to bytes. The encrypt_token function takes care of encoding the string to bytes before encrypting it, so we don't have to worry about that in the rest of our code.
# Why return the encrypted token as a string and not bytes? Because the encrypted token is typically 
def encrypt_token(token: str) -> str:
    encrypted = fernet.encrypt(token.encode())

    return encrypted.decode()


# the decrypt_token function takes an encrypted token as input, decrypts it using the Fernet object, and returns the decrypted token as a string.
def decrypt_token(encrypted_token: str) -> str:
    decrypted = fernet.decrypt(encrypted_token.encode())

    return decrypted.decode()


