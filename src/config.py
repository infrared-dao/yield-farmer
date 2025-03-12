import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL", "https://rpc.berachain.com")  # Mainnet RPC
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

TOKENS = {
    "WBTC": {
        "addr": "0x0555E30da8f98308EdB960aa94C0Db47230d2B9c", 
        "decimals": 8
    },
    "WETH": {
        "addr": "0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590",
        "decimals": 18
    },
    "HONEY": {
        "addr": "0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        "decimals": 18
    },
    "WBERA": {
        "addr": "0x6969696969696969696969696969696969696969",  # Wrapped BERA
        "decimals": 18
    },
    "BGT": {
        "addr": "0x656b95E550C07a9ffe548bd4085c72418Ceb1dba",
        "decimals": 18
    }
}

# Balancer Vault (for swap execution)
VAULT = "0x4Be03f781C497A489E3cB0287833452cA9B9E80B"
VAULT_ABI = [
    {
        "inputs": [
            {"components": [
                {"name": "poolId", "type": "bytes32"},
                {"name": "kind", "type": "uint8"},
                {"name": "assetIn", "type": "address"},
                {"name": "assetOut", "type": "address"},
                {"name": "amount", "type": "uint256"},
                {"name": "userData", "type": "bytes"}
            ], "name": "singleSwap", "type": "tuple"},
            {"name": "funds", "components": [
                {"name": "sender", "type": "address"},
                {"name": "fromInternalBalance", "type": "bool"},
                {"name": "recipient", "type": "address"},
                {"name": "toInternalBalance", "type": "bool"}
            ], "type": "tuple"},
            {"name": "limit", "type": "uint256"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "swap",
        "outputs": [{"name": "amountCalculated", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Balancer Vault Query contract (from berascan.com)
VAULT_QUERY = "0x3C612e132624f4Bd500eE1495F54565F0bcc9b59"
VAULT_QUERY_ABI = [
    {
        "inputs": [
            {"components": [
                {"name": "poolId", "type": "bytes32"},
                {"name": "kind", "type": "uint8"},
                {"name": "assetIn", "type": "address"},
                {"name": "assetOut", "type": "address"},
                {"name": "amount", "type": "uint256"},
                {"name": "userData", "type": "bytes"}
            ], "name": "request", "type": "tuple"},
            {"name": "funds", "components": [
                {"name": "sender", "type": "address"},
                {"name": "fromInternalBalance", "type": "bool"},
                {"name": "recipient", "type": "address"},
                {"name": "toInternalBalance", "type": "bool"}
            ], "type": "tuple"},
        ],
        "name": "querySwap",
        "outputs": [{"name": "amount", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Beraswap pool IDs (placeholders, update from BEX docs or Beratrail)
POOL_IDS = {
    "WBTC_WBERA": "0x38fdd999fe8783037db1bbfe465759e312f2d809000200000000000000000004",  # Bytes32 ID for WBTC/WBERA pool
    "WETH_WBERA": "0xdd70a5ef7d8cfe5c5134b5f9874b09fb5ce812b4000200000000000000000003",  # Bytes32 ID for WETH/WBERA pool
    "HONEY_WBERA": "0x2c4a603a2aa5596287a06886862dc29d56dbc354000200000000000000000002"  # Bytes32 ID for HONEY/WBERA pool (not WBERA/HONEY in docs)
}


# Minimal ERC-20 ABI for allowance and approve
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "user", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]

MIN_TRADE_AMOUNT = 0.0001

# Infrared Vault ABI (simplified for getReward and stake)
INFRARED_VAULT_ABI = [
    {
        "constant": False,
        "inputs": [],
        "name": "getReward",
        "outputs": [],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "stake",
        "outputs": [],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "user", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]

# iBGT token address
iBGT_ADDRESS = "0xac03CABA51e17c86c921E1f6CBFBdC91F8BB2E6b"

# Infrared vaults
VAULTS = {
    "WBTC_WBERA": "0x78beda3a06443f51718d746aDe95b5fAc094633E",  # Infrared vault for WBTC/WBERA LP
    "WETH_WBERA": "0x0dF14916796854d899576CBde69a35bAFb923c22",  # Infrared vault for WETH/WBERA LP
    "HONEY_WBERA": "0xe2d8941dfb85435419D90397b09D18024ebeef2C",  # Infrared vault for HONEY/WBERA LP
    "iBGT": "0x75F3Be06b02E235f6d0E7EF2D462b29739168301" 
}

# iBGT Vault address (update with mainnet value)
iBGT_VAULT = "0x75F3Be06b02E235f6d0E7EF2D462b29739168301"