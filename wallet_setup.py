import json
import blockcypher

# Load API key from api.json
with open("api.json", "r") as f:
    api_data = json.load(f)
    api_key = api_data["api_key"]

# Generate a new random private key
new_key = blockcypher.generate_new_address('btc', api_key=api_key)['private']

# Get the corresponding Bitcoin address
new_address = blockcypher.generate_new_address('btc', api_key=api_key)['address']

# Print and save the wallet address
print("New address:", new_address)
with open("wallet.json", "w") as f:
    json.dump({"address": new_address}, f)

# Save the private key in private_key.json
with open("private_key.json", "w") as f:
    json.dump({"private_key": new_key}, f)

print("Wallet address and private key saved successfully.")
