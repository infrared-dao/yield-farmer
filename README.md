# Yield Farming Bot

A Python script designed to automate yield farming on the Infrared protocol. This bot harvests `iBGT` rewards from specified vaults and stakes them into the `iBGTVault`. It includes logging for monitoring, error handling for robustness, and integration with Ethereum blockchain via Web3.py.

## Features
- Harvests iBGT rewards from multiple Infrared vaults.
- Automatically stakes harvested iBGT into the `iBGTVault`.
- Configurable minimum iBGT amount to avoid dust transactions.
- Comprehensive logging for debugging and monitoring.

## Prerequisites
- **Python 3.12+**: Ensure Python is installed on your system.
- **Poetry**: Used for dependency management (install via `pip install poetry` or follow [official instructions](https://python-poetry.org/docs/#installation)).
- **Berachain Node**: Access to a Berachain node (e.g., Alchemy or a local node).
- **Account Private Key**: A funded Ethereum account with iBGT tokens for transactions.


## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/infrared-dao/yield-farmer.git
   cd yield-farming-bot
   ```

2. **Install Dependencies with Poetry**
    ```bash
    poetry install
    ```

3. **Set Up Environment Variables**
    Create a `.env` file in the project root and add the following:
    ```
    PRIVATE_KEY=your_berachain_private_key
    RPC_URL=https://rpc.berachain.com  # Or other RPC URL
    ```

4. **Add Vaults of interest**
    Add any vaults of interest, not already included in `src/config.py`

## Usage

Run once to check.
```bash
poetry run python -m src.yield_farm
```

The bot will:
- Harvest rewards from all configured vaults.
- Check the `iBGT` balance and approve the vault if necessary.
- Stake any harvested `iBGT` above the minimum threshold (0.0001 iBGT by default).

To schedule to run routinely.
```bash
chmod +x shell/run_yield_farmer.sh
./shell/run_yield_farmer.sh
```

## Disclaimer
This script interacts with blockchain contracts and involves financial transactions. Use at your own risk. Ensure you understand the code and test thoroughly before deploying with real funds.



