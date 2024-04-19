import socket
import threading
import tkinter as tk

# File to store chat history
chat_history_file = "chat_history.txt"

# List to store owner messages
owner_messages = []

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            # Display received message
            display_message(message)
            if message.lower() == "exit":
                print("Exiting...")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to display messages in the chat window
def display_message(message):
    username, message_content = message.split(":", 1)
    align = "left" if username.strip() == client_username.strip() else "left"
    # Check if message is from the owner and if it's already displayed
    if align == "left":
        if message_content.strip() in owner_messages:
            owner_messages.remove(message_content.strip())
            return  # Skip displaying the message again if it's in the list
        else:
            owner_messages.append(message_content.strip())
    # Insert message into chat history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"{username}: {message_content.strip()}\n", align)
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

# Function to send messages to the server
def send_message(event=None):
    message = message_entry.get()
    if message:
        client.send(f"{client_username}: {message}".encode())
        if message.lower() == "exit":
            print("Exiting...")
            client.close()
            root.quit()
            return
        display_message(f"{client_username}: {message}")
        message_entry.delete(0, tk.END)

# Function to set username
def set_username():
    global client_username
    client_username = username_entry.get()
    if client_username:
        username_frame.destroy()
        connect_to_server()

# Function to show chat history
def show_chat_history():
    # Open and read the chat history file
    with open(chat_history_file, "r") as file:
        chat_content = file.read()
    # Display chat history in a new window
    chat_window = tk.Toplevel(root)
    chat_window.title("Chat History")
    chat_text = tk.Text(chat_window)
    chat_text.insert(tk.END, chat_content)
    chat_text.pack()

# Function to connect to the server
def connect_to_server():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    chat_frame.pack()

# Define host and port
host = "127.0.0.1"
port = 5555
client_username = None

# Create the main window
root = tk.Tk()
root.title("Chat Application")

# Create username entry frame
username_frame = tk.Frame(root)
username_frame.pack(padx=10, pady=10)

# Create username entry label
username_label = tk.Label(username_frame, text="Enter your username:")
username_label.grid(row=0, column=0)

# Create username entry field
username_entry = tk.Entry(username_frame, width=30)
username_entry.grid(row=0, column=1)

# Create set username button
username_button = tk.Button(username_frame, text="Set Username", command=set_username)
username_button.grid(row=0, column=2)

# Create chat frame
chat_frame = tk.Frame(root)

# Create chat history text widget
chat_history = tk.Text(chat_frame, height=20, width=50)
chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
chat_history.config(state=tk.DISABLED)

# Create message entry field
message_entry = tk.Entry(chat_frame, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)
message_entry.bind("<Return>", send_message)

# Create send message button
send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Create button to show chat history
show_history_button = tk.Button(root, text="Show Chat History", command=show_chat_history)
show_history_button.pack()

# Start the application
root.mainloop()
