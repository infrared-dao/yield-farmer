from web3 import Web3

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

def get_balance(token_addr, account_addr):
    token = w3.eth.contract(address=token_addr, abi=[{"constant": True, "inputs": [{"name": "_owner", "type": "address"}],"name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],"type": "function"}])
    return token.functions.balanceOf(account_addr).call() / 1e18

def gas_check(max_gwei):
    return w3.eth.gas_price < w3.to_wei(max_gwei, "gwei")