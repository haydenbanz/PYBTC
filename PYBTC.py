import tkinter as tk
import blockcypher
import json
import webbrowser






# Load the API key from api.json
with open('api.json', 'r') as f:
    api_data = json.load(f)
    API_KEY = api_data['api_key']
	
	
	
#keys
with open('private_key.json', 'r') as f:
    private_key_data = json.load(f)
    private_key = private_key_data['private_key']

def run_file_1():
    # Generate a new random private key
    new_key = blockcypher.generate_new_address('btc', api_key=API_KEY)['private']

    # Get the corresponding Bitcoin address
    new_address = blockcypher.generate_new_address('btc', api_key=API_KEY)['address']

    # Update the label text with the Bitcoin address
    label.config(text="Your BTC Address: " + new_address)

def run_file_2():
    # Create a new window for sending BTC
    send_window = tk.Toplevel(pybtc)
    send_window.title("Send BTC")

    # Create a label and entry for entering the address
    address_label = tk.Label(send_window, text="To Address:")
    address_label.pack()
    address_entry = tk.Entry(send_window)
    address_entry.pack()

    # Create a label and entry for entering the amount
    amount_label = tk.Label(send_window, text="Amount:")
    amount_label.pack()
    amount_entry = tk.Entry(send_window)
    amount_entry.pack()

    # Function to handle the send button click
    def send_button_click():
        # Get the address and amount from the entries
        to_address = address_entry.get()
        amount = float(amount_entry.get())
        
        # Load the wallet address and private key from wallet.json
        with open('wallet.json', 'r') as f:
            wallet_data = json.load(f)
            address = wallet_data['address']
            
        
        # Create the transaction
        inputs = [{'address': address}]
        outputs = [{'address': to_address, 'value': int(amount * 100000000)}]

        unsigned_tx = blockcypher.create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc')
        signed_tx = blockcypher.sign_tx(unsigned_tx, wifs=private_key, coin_symbol='btc')
        broadcasted_tx = blockcypher.broadcast_signed_transaction(signed_tx, coin_symbol='btc')

        # Update the label text with the transaction status
        result_label.config(text="Transaction sent!")

    # Create a send button
    send_button = tk.Button(send_window, text="Send", command=send_button_click)
    send_button.pack()

    # Create a label to display the transaction status
    result_label = tk.Label(send_window, text="")
    result_label.pack()

def run_file_3():
 
    with open('wallet.json', 'r') as f:
        wallet_data = json.load(f)
        address = wallet_data['address']

    balance = blockcypher.get_total_balance(address, coin_symbol='btc')

    # Update the label text with the BTC balance
    label.config(text="Your BTC Balance: {} BTC".format(balance / 100000000))
    # Create a new window for displaying transactions
    transaction_window = tk.Toplevel(pybtc)
    transaction_window.title("Transaction Details")

    # Create a text widget with scrollbar for displaying transaction details
    text_widget = tk.Text(transaction_window, height=10, width=50)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(transaction_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_widget.yview)

    # Retrieve and display transaction details
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

def run_file_4():
    # Add your code to run the fourth Python file here
   
    webbrowser.open("https://www.blockcypher.com/")
def run_file_5():
    # Open the browser with the specified URL
    webbrowser.open("haydenbanz.github.io/")
# Create the main window
pybtc = tk.Tk()

# Set the window title
pybtc.title("PY BTC WALLET")

# Set the window icon
icon = tk.PhotoImage(file='info.png')
pybtc.iconphoto(False, icon)
pybtc.geometry("600x100") 

# Create a frame to hold the buttons and label
frame = tk.Frame(pybtc)
frame.pack()

# Load the images
imagee = tk.PhotoImage(file="generate.png")
imager = tk.PhotoImage(file="send.png")
imaget = tk.PhotoImage(file="wallet.png")
imagetw = tk.PhotoImage(file="key.png")
imagepw = tk.PhotoImage(file="web.png")

# Create the buttons with the images
button1 = tk.Button(frame, image=imagee, command=run_file_1)
button2 = tk.Button(frame, image=imager, command=run_file_2)
button3 = tk.Button(frame, image=imaget, command=run_file_3)
button4 = tk.Button(frame, image=imagetw, command=run_file_4)
button5 = tk.Button(frame, image=imagepw, command=run_file_5)

# Pack the buttons horizontally in the frame
button1.pack(side=tk.LEFT)
button2.pack(side=tk.LEFT)
button3.pack(side=tk.LEFT)
button4.pack(side=tk.LEFT)
button5.pack(side=tk.LEFT)

# Create a label to display the BTC address
label = tk.Label(pybtc, text="Your BTC Address: ")
label.pack()



# Start the main GUI loop
pybtc.mainloop()
