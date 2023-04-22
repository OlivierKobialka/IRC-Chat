import socket
import threading

host = "127.0.0.1"  # localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message.startswith("MSG:"):
                broadcast(message[4:].encode("ascii"), client)
            elif message.startswith("QUIT"):
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname} left the chat!".encode("ascii"), None)
                nicknames.remove(nickname)
                break
            elif message.startswith("JOIN:"):
                nickname = message[5:]
                nicknames.append(nickname)
                clients.append(client)
                print(f"User {nickname} joined the chat!")
                broadcast(f"{nickname} joined the chat!".encode("ascii"), client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode("ascii"), None)
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"User {nickname} joined the chat!")
        broadcast(f"{nickname} joined the chat!".encode("ascii"), client)
        client.send(
            "Connected to the server! (type 'quit' to exit from chat)".encode("ascii")
        )

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()

# import socket
# import threading

# host = "127.0.0.1"  # localhost
# port = 55555

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen()

# clients = []
# nicknames = []


# def broadcast(message):
# 	for client in clients:
# 		client.send(message)


# def handle(client):
# 	while True:
# 		try:
# 			message = client.recv(1024)
# 			broadcast(message)
# 		except:
# 			index = clients.index(client)
# 			clients.remove(client)
# 			client.close()
# 			nickname = nicknames[index]
# 			broadcast(f"{nickname} left the chat!".encode("ascii"))
# 			nicknames.remove(nickname)

# 			break


# def receive():
# 	while True:
# 		client, address = server.accept()
# 		print(f"Connected with {str(address)}")

# 		client.send("NICK".encode("ascii"))
# 		nickname = client.recv(1024).decode("ascii")
# 		nicknames.append(nickname)
# 		clients.append(client)

# 		print(f"User {nickname} joined the chat!")
# 		broadcast(f"{nickname} joined the chat!".encode("ascii"))
# 		client.send("Connected to the server! (type 'quit' to exit from chat)".encode("ascii"))

# 		thread = threading.Thread(target=handle, args=(client,))
# 		thread.start()


# print("Server is listening...")
# receive()
