from web3 import Web3
import os
from dotenv import load_dotenv
from src.logging_setup import setup_logging

load_dotenv()
logger = setup_logging("blockchain")

class Blockchain:
    def __init__(self):
        self.w3 = None
        self.account = None
        self.connect()

    def connect(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
            if not self.w3.is_connected():
                raise ConnectionError("RPC not connected")
            self.account = self.w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
            logger.info("Blockchain connected")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise

    def get_balance(self, token_addr, decimals=18):
        try:
            token = self.w3.eth.contract(address=token_addr, abi=[{"constant": True, "inputs": [{"name": "_owner", "type": "address"}],"name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],"type": "function"}])
            return token.functions.balanceOf(self.account.address).call() / 10**decimals
        except Exception as e:
            logger.error(f"Balance fetch failed: {e}")
            return 0

    def send_tx(self, tx, gas_limit=200000, max_gwei=20):
        if self.w3.eth.gas_price > self.w3.to_wei(max_gwei, "gwei"):
            logger.warning("Gas too high, skipping")
            return None
        tx["from"] = self.account.address
        tx["nonce"] = self.w3.eth.get_transaction_count(self.account.address)
        # tx["gas"] = gas_limit
        tx["gasPrice"] = self.w3.eth.gas_price
        signed_tx = self.w3.eth.account.sign_transaction(tx, os.getenv("PRIVATE_KEY"))
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        logger.info(f"Tx sent: {tx_hash.hex()}")
        return receipt