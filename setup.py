import json

# Ask for API key
api_key = input("Enter your BlockCypher API key: ")

# Save API key in api.json
with open("api.json", "w") as f:
    json.dump({"api_key": api_key}, f)

print("API key saved successfully.")
