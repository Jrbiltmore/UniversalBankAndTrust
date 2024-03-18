# UUID: 62ae5be7-8fb3-4594-bf79-e78a60eea485

# quantum_interface.py

"""
This module defines an interface for integrating quantum and post-quantum cryptographic functionalities
into the blockchain. It abstracts the complexity of quantum-resistant algorithms and quantum key
distribution (QKD) mechanisms, providing a simplified API for the rest of the blockchain system.
"""

from typing import Tuple, Optional
from .quantum_algorithms import KyberKEM, DilithiumSignature

class QuantumInterface:
    """
    Provides an interface for quantum and post-quantum cryptographic operations,
    including key generation, encryption/decryption, and signing/verification.
    """

    @staticmethod
    def generate_keypair(algorithm: str) -> Tuple[str, str]:
        """
        Generates a quantum-resistant public/private key pair based on the specified algorithm.
        """
        if algorithm.lower() == 'kyber':
            return KyberKEM.generate_keypair()
        elif algorithm.lower() == 'dilithium':
            return DilithiumSignature.generate_keypair()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    @staticmethod
    def encrypt_message(public_key: str, message: bytes, algorithm: str) -> Tuple[bytes, Optional[bytes]]:
        """
        Encrypts a message using the public key and specified algorithm. For KEM algorithms like Kyber,
        this will encapsulate a shared secret and return the encapsulation.
        """
        if algorithm.lower() == 'kyber':
            shared_secret, encapsulation = KyberKEM.encapsulate_key(public_key)
            # Assume the shared_secret is used to symmetrically encrypt the message in real usage
            return encapsulation, None
        else:
            raise ValueError(f"Encryption not supported for algorithm: {algorithm}")

    @staticmethod
    def decrypt_message(private_key: str, encapsulation: bytes, algorithm: str) -> bytes:
        """
        Decrypts a message using the private key and specified algorithm. For KEM algorithms like Kyber,
        this will decapsulate the shared secret.
        """
        if algorithm.lower() == 'kyber':
            shared_secret = KyberKEM.decapsulate_key(private_key, encapsulation)
            # Assume the shared_secret is used to symmetrically decrypt the message in real usage
            return shared_secret
        else:
            raise ValueError(f"Decryption not supported for algorithm: {algorithm}")

    @staticmethod
    def sign_message(private_key: str, message: bytes, algorithm: str) -> bytes:
        """
        Signs a message using the private key and specified algorithm.
        """
        if algorithm.lower() == 'dilithium':
            return DilithiumSignature.sign(private_key, message)
        else:
            raise ValueError(f"Signing not supported for algorithm: {algorithm}")

    @staticmethod
    def verify_signature(public_key: str, message: bytes, signature: bytes, algorithm: str) -> bool:
        """
        Verifies a signature against a message using the public key and specified algorithm.
        """
        if algorithm.lower() == 'dilithium':
            return DilithiumSignature.verify(public_key, message, signature)
        else:
            raise ValueError(f"Verification not supported for algorithm: {algorithm}")

# Example usage demonstrating the interface
if __name__ == "__main__":
    # Key generation example using Kyber
    pub_key, priv_key = QuantumInterface.generate_keypair('kyber')
    encapsulation, _ = QuantumInterface.encrypt_message(pub_key, b"Example message", 'kyber')
    shared_secret = QuantumInterface.decrypt_message(priv_key, encapsulation, 'kyber')

    # Signing and verification example using Dilithium
    sign_pub_key, sign_priv_key = QuantumInterface.generate_keypair('dilithium')
    signature = QuantumInterface.sign_message(sign_priv_key, b"Example message", 'dilithium')
    verification = QuantumInterface.verify_signature(sign_pub_key, b"Example message", signature, 'dilithium')

    print("Shared secret (Kyber):", shared_secret)
    print("Signature verified (Dilithium):", verification)
