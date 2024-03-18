# UUID: 37eb27df-86ab-4731-a91d-d4a4216ebd14
# chain.py

import hashlib
import json
from time import time
from typing import List, Dict, Any
from cryptography.exceptions import InvalidSignature
from .quantum_security import QuantumSecurity, SecurityError

class Transaction:
    def __init__(self, sender, recipient, amount, signature):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature
        }

    def verify_transaction_signature(self):
        """
        Verifies the signature of the transaction.
        """
        try:
            sender_public_key = QuantumSecurity.deserialize_public_key(self.sender)
            return QuantumSecurity.verify_signature(sender_public_key, str(self.to_dict()), self.signature)
        except (InvalidSignature, SecurityError):
            return False

class Block:
    def __init__(self, index: int, transactions: List[Dict[str, Any]], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp or time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        Computes a SHA-256 hash of the block's contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 4  # Difficulty of the Proof-of-Work algorithm

    def __init__(self):
        self.unconfirmed_transactions = []  # data yet to get into the blockchain
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates the genesis (first) block and appends it to the chain.
        """
        genesis_block = Block(0, [], time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block: Block, proof: str):
        """
        Adds a block to the chain after verification.
        Verification includes:
        - Checking that the proof is valid.
        - The previous_hash referred in the block and the hash of latest block in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block: Block, block_hash: str):
        """
        Check if block_hash is valid hash of block and satisfies the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block: Block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction: Dict[str, Any]):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def add_new_transaction(self, transaction: Transaction):
        """
        Adds a new transaction to the unconfirmed transactions pool after verification.
        """
        if transaction.verify_transaction_signature():
            self.unconfirmed_transactions.append(transaction.to_dict())
        else:
            raise SecurityError("Invalid transaction signature.")

    def execute_smart_contract(self, contract_address, action, params):
        """
        Executes a smart contract action on the blockchain.
        """
        # Placeholder for smart contract execution logic.
        # Would involve fetching the contract by address, executing the specified action
        # with given parameters, and handling state changes.
        pass

    # Update the mine method to include smart contract execution
    def mine(self):
        """
        Enhanced mining process that also executes smart contracts included in transactions.
        """
        if not self.unconfirmed_transactions:
            return False

        # Placeholder for executing smart contracts within unconfirmed transactions
        for transaction in self.unconfirmed_transactions:
            if transaction.get("is_contract"):
                self.execute_smart_contract(transaction["contract_address"],
                                            transaction["action"], transaction["params"])

        # Proceed with existing mining process
        # Additional steps...

# Consensus mechanism flexibility
class ConsensusMechanism:
    @staticmethod
    def proof_of_work(blockchain, block):
        # Implement PoW consensus algorithm
        pass

    @staticmethod
    def proof_of_stake(blockchain, block):
        # Implement PoS consensus algorithm
        pass

# The blockchain can now use a flexible consensus mechanism
blockchain.consensus_mechanism = ConsensusMechanism.proof_of_work  # or .proof_of_stake

