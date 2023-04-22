import socket
import threading

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
                if message.lower() == "quit":
                    client.close()
                    break

        except:
            print("ERROR!")
            client.close()
            break


def write():
    while True:
        message = input("")
        if message.lower() == "quit":
            client.send("QUIT".encode("ascii"))
            client.close()
            break
        else:
            client.send(f"MSG:{message}".encode("ascii"))


recive_thread = threading.Thread(target=receive)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

# import socket
# import threading

# nickname = input("Choose your nickname: ")

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("127.0.0.1", 55555))


# def receive():
#     while True:
#         try:
#             message = client.recv(1024).decode("ascii")
#             if message == "NICK":
#                 client.send(nickname.encode("ascii"))
#             else:
#                 print(message)
#                 if message.lower() == "quit":
#                     client.close()
#                     break

#         except:
#             print("ERROR!")
#             client.close()
#             break


# def write():
#     while True:
#         message = f'{nickname}: {input("")}'
#         client.send(message.encode("ascii"))


# recive_thread = threading.Thread(target=receive)
# recive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()
