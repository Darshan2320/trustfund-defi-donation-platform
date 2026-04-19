# TrustFund Donation Analytics Script
# Connects to Ethereum Sepolia testnet and retrieves donation data
# from the deployed DonationVault smart contract.

from web3 import Web3

# ─── Configuration ───────────────────────────────────────────────
SEPOLIA_RPC = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0x99981d896E445eCeEb90D3FFcFee6bD0FD35Ce22"

# Contract ABI (only the parts we need for analytics)
ABI = [
    {
        "inputs": [],
        "name": "totalRaised",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "donationCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getContractBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "donorTotal",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "donor", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "DonationReceived",
        "type": "event"
    }
]

# ─── Connect to Sepolia ───────────────────────────────────────────
print("=" * 55)
print("   TrustFund Donation Analytics")
print("=" * 55)

web3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

if web3.is_connected():
    print("✅ Connected to Ethereum Sepolia Testnet")
else:
    print("❌ Connection failed")
    exit()

# ─── Load Contract ────────────────────────────────────────────────
contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=ABI
)

# ─── Read Contract Data ───────────────────────────────────────────
total_raised = contract.functions.totalRaised().call()
donation_count = contract.functions.donationCount().call()
contract_balance = contract.functions.getContractBalance().call()

print()
print("📊 Campaign Statistics")
print("-" * 40)
print(f"Total Raised:      {web3.from_wei(total_raised, 'ether')} ETH")
print(f"Contract Balance:  {web3.from_wei(contract_balance, 'ether')} ETH")
print(f"Total Donations:   {donation_count}")

# ─── Read Donation Events ─────────────────────────────────────────
print()
print("📋 Donation History")
print("-" * 40)

events = contract.events.DonationReceived.get_logs(from_block=0)

if len(events) == 0:
    print("No donations found.")
else:
    donor_totals = {}

    for event in events:
        donor = event['args']['donor']
        amount = event['args']['amount']
        amount_eth = web3.from_wei(amount, 'ether')

        print(f"Donor:  {donor}")
        print(f"Amount: {amount_eth} ETH")
        print("-" * 40)

        if donor in donor_totals:
            donor_totals[donor] += amount
        else:
            donor_totals[donor] = amount

    # ─── Donor Summary ────────────────────────────────────────────
    print()
    print("🏆 Donor Summary")
    print("-" * 40)
    print(f"Unique Donors: {len(donor_totals)}")
    print()

    for donor, total in donor_totals.items():
        print(f"Wallet: {donor}")
        print(f"Total:  {web3.from_wei(total, 'ether')} ETH")
        print("-" * 40)

print()
print("Analytics complete.")
print("=" * 55)
