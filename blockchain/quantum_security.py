import os
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecurityError(Exception):
    """
    Custom exception for security-related errors.
    """
    pass

def is_valid_nonce(nonce):
    """
    Validates the nonce to ensure it meets expected criteria (e.g., length).
    """
    return isinstance(nonce, bytes) and len(nonce) == 12

def sanitize_public_key(their_public_key):
    """
    Sanitizes the public key input to prevent code injection and ensure it is a valid X25519 public key.
    Placeholder for public key sanitization and validation logic.
    """
    # In a real scenario, additional validation to ensure the public key is in the correct format
    # and not maliciously crafted would be performed here.
    return their_public_key

def encrypt_data(public_key, data, my_private_key):
    """
    Encrypts data using a hybrid encryption scheme. This example uses X25519 for key exchange,
    HKDF for key derivation, and AES-GCM for symmetric encryption.
    """
    if not isinstance(public_key, X25519PublicKey):
        raise ValueError("Public key must be an instance of X25519PublicKey.")
    
    shared_secret = my_private_key.exchange(public_key)
    
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'quantum-safe encryption',
    ).derive(shared_secret)
    
    aesgcm = AESGCM(derived_key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    
    return encrypted_data, nonce

def decrypt_data(private_key, encrypted_data, nonce, their_public_key):
    """
    Decrypts data using a hybrid encryption scheme, with added input sanitization.
    """
    if not isinstance(private_key, X25519PrivateKey):
        raise ValueError("Private key must be an instance of X25519PrivateKey.")
    
    if not is_valid_nonce(nonce):
        raise ValueError("Invalid nonce provided.")
    their_public_key = sanitize_public_key(their_public_key)
    
    shared_secret = private_key.exchange(their_public_key)
    
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'quantum-safe encryption',
    ).derive(shared_secret)
    
    aesgcm = AESGCM(derived_key)
    try:
        decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
    except Exception as e:
        raise SecurityError(f"Decryption failed: {e}")
    
    return decrypted_data
