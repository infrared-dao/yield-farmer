import json
import time
from src.blockchain import Blockchain
from src.logging_setup import setup_logging
from src.config import *

# Constants
MIN_iBGT_AMOUNT = 0.0001  # Minimum iBGT amount to stake (avoid dust)

# Initialize logger, bot, and blockchain
logger = setup_logging("yield_farm")
bc = Blockchain()

def harvest_vaults():
    """Harvest iBGT rewards from Infrared vaults."""
    logger.info("Starting vault harvest process")

    for pool_name, vault_address in VAULTS.items():
        logger.info(f"Harvesting rewards from vault: {pool_name} ({vault_address})")
        vault_contract = bc.w3.eth.contract(address=vault_address, abi=INFRARED_VAULT_ABI)

        # Check stake balance before harvesting
        try:
            stake_balance = vault_contract.functions.balanceOf(bc.account.address).call()
            logger.info(f"Stake balance for {pool_name}: {stake_balance / 10**18:.6f} ")
            if stake_balance < MIN_iBGT_AMOUNT * 10**18:
                logger.info(f"Skipping harvest for {pool_name}: stake balance {stake_balance / 10**18:.6f} below minimum {MIN_iBGT_AMOUNT}")
                continue
        except Exception as e:
            logger.error(f"Failed to check balance for {pool_name}: {str(e)}")
            continue
        
        try:
            tx = vault_contract.functions.getReward().build_transaction({
                "from": bc.account.address,
                "nonce": bc.w3.eth.get_transaction_count(bc.account.address),
                "gas": 400000,
                "gasPrice": bc.w3.eth.gas_price
            })
            receipt = bc.send_tx(tx)
            if receipt and receipt.status == 1:
                # Estimate iBGT harvested (requires event parsing or balance check)
                logger.info(f"Successfully harvested rewards from {pool_name}")
            else:
                logger.error(f"Harvest failed for {pool_name}: transaction reverted")
        except Exception as e:
            logger.error(f"Harvest failed for {pool_name}: {str(e)}")
    return True

def stake_iBGT(amount):
    """Stake iBGT into the iBGTVault."""
    logger.info(f"Staking iBGT: Amount={amount / 10**18:.6f}")
    if amount < MIN_iBGT_AMOUNT * 10**18:
        logger.warning(f"iBGT amount {amount / 10**18:.6f} below minimum {MIN_iBGT_AMOUNT}, skipping")
        return False

    ibgt_vault_contract = bc.w3.eth.contract(address=iBGT_VAULT, abi=INFRARED_VAULT_ABI)
    try:
        tx = ibgt_vault_contract.functions.stake(int(amount)).build_transaction({
            "from": bc.account.address,
            "nonce": bc.w3.eth.get_transaction_count(bc.account.address),
            "gas": 300000,
            "gasPrice": bc.w3.eth.gas_price
        })
        receipt = bc.send_tx(tx)
        if receipt and receipt.status == 1:
            logger.info(f"Successfully staked {amount / 10**18:.6f} iBGT into iBGTVault")
            return True
        else:
            logger.error("iBGT staking failed: transaction reverted")
            return False
    except Exception as e:
        logger.error(f"iBGT staking failed: {str(e)}")
        return False

def approve_iBGT_vault():
    """Approve iBGTVault to spend iBGT if allowance is insufficient."""
    logger.info("Checking iBGT allowance for iBGTVault")
    ibgt_contract = bc.w3.eth.contract(address=iBGT_ADDRESS, abi=ERC20_ABI)
    allowance = ibgt_contract.functions.allowance(bc.account.address, iBGT_VAULT).call()
    logger.info(f"Current iBGT allowance: {allowance / 10**18:.2f} iBGT")

    if allowance < 10**18:  # Less than 1 iBGT
        logger.info("Approving iBGTVault for iBGT")
        max_amount = 2**256 - 1
        tx = ibgt_contract.functions.approve(iBGT_VAULT, max_amount).build_transaction({
            "from": bc.account.address,
            "nonce": bc.w3.eth.get_transaction_count(bc.account.address),
            "gas": 100000,
            "gasPrice": bc.w3.eth.gas_price
        })
        try:
            receipt = bc.send_tx(tx)
            if receipt and receipt.status == 1:
                logger.info("iBGTVault approved to spend max iBGT")
            else:
                logger.error("iBGT approval failed: transaction reverted")
        except Exception as e:
            logger.error(f"iBGT approval failed: {str(e)}")

def yield_farm():
    """Harvest rewards from Infrared vaults and stake iBGT."""
    logger.info("Starting yield farming process")
    
    # Step 1: Harvest rewards from vaults
    harvest_vaults()
    
    # Step 2: Check iBGT balance and approve vault if needed
    ibgt_contract = bc.w3.eth.contract(address=iBGT_ADDRESS, abi=ERC20_ABI)
    ibgt_balance = ibgt_contract.functions.balanceOf(bc.account.address).call()
    logger.info(f"Current iBGT balance: {ibgt_balance / 10**18:.6f}")
    
    if ibgt_balance > MIN_iBGT_AMOUNT * 10**18:
        approve_iBGT_vault()
        
        # Step 3: Stake harvested iBGT
        if stake_iBGT(ibgt_balance):
            logger.info("Yield farming cycle completed successfully")
        else:
            logger.error("Yield farming cycle failed during staking")
    else:
        logger.info("No significant iBGT to stake, skipping")

if __name__ == "__main__":
    try:
        yield_farm()
    except Exception as e:
        logger.error(f"Yield farming process crashed: {str(e)}")