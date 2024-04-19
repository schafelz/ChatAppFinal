import socket
import threading

# Function to handle client connections
def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode()
            if not message:
                break
            # Print received message
            print(f"Received message from {address}: {message}")
            # Check if message is 'exit' to close connection
            if message.lower() == "exit":
                client_socket.send("exit".encode())
                break
            # Save message to chat history file
            save_message(message)
            # Broadcast message to all clients
            broadcast(message)
        except Exception as e:
            # Handle any errors that occur
            print(f"Error: {e}")
            break

    # Close client connection
    print(f"Connection from {address} closed.")
    client_socket.close()
    # Remove client from list of clients
    if client_socket in clients:
        clients.remove(client_socket)

# Function to save message to chat history file
def save_message(message):
    with open("chat_history.txt", "a") as file:
        file.write(f"{message}\n")

# Function to broadcast message to all clients
def broadcast(message):
    for client in clients:
        try:
            # Send message to client
            client.send(message.encode())
        except:
            # Close client connection if unable to send message
            client.close()
            clients.remove(client)

# Define host and port
host = "127.0.0.1"
port = 5555

# Create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to host and port
server.bind((host, port))
# Listen for incoming connections
server.listen(5)

# Print server info
print(f"Server listening on {host}:{port}")

# List to store client sockets
clients = []

# Main loop to accept incoming connections
while True:
    # Accept client connection
    client_socket, address = server.accept()
    # Add client socket to list of clients
    clients.append(client_socket)
    # Create a new thread to handle client communication
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
