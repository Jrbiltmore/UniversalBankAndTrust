import os
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key, load_der_public_key, PublicFormat, Encoding
)
from cryptography.exceptions import InvalidKey

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass

def is_valid_raw_public_key(key_bytes):
    """Check if raw public key bytes represent a valid X25519 public key."""
    return len(key_bytes) == 32

def sanitize_public_key(public_key_input):
    """
    Validates and sanitizes the public key input, supporting both PEM and raw formats.
    Ensures it is a valid X25519 public key.
    """
    try:
        if isinstance(public_key_input, str) or (isinstance(public_key_input, bytes) and b"-----BEGIN" in public_key_input):
            public_key = load_pem_public_key(public_key_input)
        elif isinstance(public_key_input, bytes) and is_valid_raw_public_key(public_key_input):
            public_key = load_der_public_key(public_key_input)
        else:
            raise ValueError("Unsupported public key input format.")
        if not isinstance(public_key, X25519PublicKey):
            raise ValueError("The provided public key is not a valid X25519 public key.")
        return public_key
    except (ValueError, InvalidKey, TypeError) as e:
        raise SecurityError(f"Invalid public key provided: {e}")

def encrypt_data(public_key, data, my_private_key):
    """
    Encrypts data using a hybrid encryption scheme with X25519, HKDF, and AES-GCM.
    """
    if not isinstance(public_key, X25519PublicKey):
        raise ValueError("Public key must be an instance of X25519PublicKey.")
    
    shared_secret = my_private_key.exchange(public_key)
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'quantum-safe encryption').derive(shared_secret)
    aesgcm = AESGCM(derived_key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    return encrypted_data, nonce

def decrypt_data(private_key, encrypted_data, nonce, their_public_key):
    """
    Decrypts data using a hybrid encryption scheme with input sanitization.
    """
    if not isinstance(private_key, X25519PrivateKey):
        raise ValueError("Private key must be an instance of X25519PrivateKey.")
    
    if not is_valid_nonce(nonce):
        raise ValueError("Invalid nonce provided.")
    their_public_key = sanitize_public_key(their_public_key)
    
    shared_secret = private_key.exchange(their_public_key)
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'quantum-safe encryption').derive(shared_secret)
    aesgcm = AESGCM(derived_key)
    try:
        decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
    except Exception as e:
        raise SecurityError(f"Decryption failed: {e}")
    return decrypted_data

# Example usage and validation
try:
    # Placeholder for actual key generation and data encryption/decryption operations
    my_private_key = X25519PrivateKey.generate()
    their_public_key = my_private_key.public_key()  # In real use, this would be the recipient's public key
    public_key_input = their_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    
    sanitized_public_key = sanitize_public_key(public_key_input)
    data = b"Secret message"
    encrypted_data, nonce = encrypt_data(sanitized_public_key, data, my_private_key)
    decrypted_data = decrypt_data(my_private_key, encrypted_data, nonce, sanitized_public_key)
    assert data == decrypted_data
    print("Encryption and decryption were successful.")
except SecurityError as e:
    print(e)
