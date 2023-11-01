import tkinter as tk
import blockcypher
import json
import webbrowser

# Load the API key from api.json
with open('api.json', 'r') as f:
    api_data = json.load(f)
    API_KEY = api_data['api_key']

# Load the private key
with open('private_key.json', 'r') as f:
    private_key_data = json.load(f)
    private_key = private_key_data['private_key']

# Function to generate a new Bitcoin address
def generate_new_address():
    new_key = blockcypher.generate_new_address('btc', api_key=API_KEY)['private']
    new_address = blockcypher.generate_new_address('btc', api_key=API_KEY)['address']
    label.config(text="Your BTC Address: " + new_address)

# Function to send BTC
def send_btc():
    send_window = tk.Toplevel(pybtc)
    send_window.title("Send BTC")

    address_label = tk.Label(send_window, text="To Address:")
    address_label.pack()
    address_entry = tk.Entry(send_window)
    address_entry.pack()

    amount_label = tk.Label(send_window, text="Amount:")
    amount_label.pack()
    amount_entry = tk.Entry(send_window)
    amount_entry.pack()

    def send_button_click():
        to_address = address_entry.get()
        amount = float(amount_entry.get())

        with open('wallet.json', 'r') as f:
            wallet_data = json.load(f)
            address = wallet_data['address']

        inputs = [{'address': address}]
        outputs = [{'address': to_address, 'value': int(amount * 100000000)}]

        unsigned_tx = blockcypher.create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc')
        signed_tx = blockcypher.sign_tx(unsigned_tx, wifs=private_key, coin_symbol='btc')
        broadcasted_tx = blockcypher.broadcast_signed_transaction(signed_tx, coin_symbol='btc')

        result_label.config(text="Transaction sent!")

    send_button = tk.Button(send_window, text="Send", command=send_button_click)
    send_button.pack()

    result_label = tk.Label(send_window, text="")
    result_label.pack()

# Function to display balance and transactions
def display_balance_and_transactions():
    with open('wallet.json', 'r') as f:
        wallet_data = json.load(f)
        address = wallet_data['address']

    balance = blockcypher.get_total_balance(address, coin_symbol='btc')
    label.config(text="Your BTC Balance: {} BTC".format(balance / 100000000))

    transaction_window = tk.Toplevel(pybtc)
    transaction_window.title("Transaction Details")

    text_widget = tk.Text(transaction_window, height=10, width=50)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(transaction_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_widget.yview)

    transactions = blockcypher.get_address_details(address, coin_symbol='btc')['txrefs']

    if transactions:
        for tx in transactions:
            text_widget.insert(tk.END, "Transaction Hash: {}\n".format(tx['tx_hash']))
            text_widget.insert(tk.END, "Block Height: {}\n".format(tx['block_height']))
            text_widget.insert(tk.END, "Confirmed: {}\n".format(tx['confirmed']))
            text_widget.insert(tk.END, "-------------------------------------\n")
    else:
        text_widget.insert(tk.END, "No transactions found.")

    text_widget.config(state=tk.DISABLED)

# Function to open a web page
def open_webpage(url):
    webbrowser.open(url)

# Create the main window
pybtc = tk.Tk()
pybtc.title("PY BTC WALLET")

# Load images for buttons
generate_image = tk.PhotoImage(file="generate.png")
send_image = tk.PhotoImage(file="send.png")
wallet_image = tk.PhotoImage(file="wallet.png")
key_image = tk.PhotoImage(file="key.png")
web_image = tk.PhotoImage(file="web.png")

# Create a frame to hold the buttons and label
frame = tk.Frame(pybtc)
frame.pack()

# Create and configure buttons with images
generate_button = tk.Button(frame, image=generate_image, command=generate_new_address)
send_button = tk.Button(frame, image=send_image, command=send_btc)
wallet_button = tk.Button(frame, image=wallet_image, command=display_balance_and_transactions)
key_button = tk.Button(frame, image=key_image, command=lambda: open_webpage("https://www.blockcypher.com/"))
web_button = tk.Button(frame, image=web_image, command=lambda: open_webpage("https://haydenbanz.github.io/pybtc"))

# Pack the buttons horizontally in the frame
generate_button.pack(side=tk.LEFT)
send_button.pack(side=tk.LEFT)
wallet_button.pack(side=tk.LEFT)
key_button.pack(side=tk.LEFT)
web_button.pack(side=tk.LEFT)

# Create a label to display the BTC address
label = tk.Label(pybtc, text="Your BTC Address: ")
label.pack()

# Start the main GUI loop
pybtc.mainloop()
