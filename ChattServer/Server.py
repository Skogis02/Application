import socket
import threading
import sys

#User as tuple (Name, Socket, Address(IP, Port))

IP = "127.0.0.1"
PORT = 5050
SERVER_ADDR = (IP, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(SERVER_ADDR)
FORMAT = "utf-8"
HEADER = 10
users = []

def search_user(search_string, par):
    for user in users:
        if user[par] == search_string:
            return user, True
    return "", False

def get_user_list():
    user_list = "Online users:"
    for user in users:
        user_list += str("\n" + user[0])
    return user_list

def receive(user):
    validlen = False
    while validlen == False:
        try:
            msg_len = int(user[1].recv(HEADER).decode(FORMAT))
            validlen = True
        except:
            validlen = False
    return str(user[1].recv(msg_len).decode(FORMAT))

def send(user, msg):
    if msg == "":
        return
    msg_byte = msg.encode(FORMAT)
    msg_len = len(msg_byte)
    msg_len_byte = str(msg_len).encode(FORMAT)
    msg_len_byte += b" "*(HEADER - len(msg_len_byte))
    user[1].send(msg_len_byte)
    user[1].send(msg_byte)
    return

def new_user(user_socket, user_addr):
    user = ("", user_socket, user_addr)
    send(user, "Please provide a username:")
    validname = False
    while not validname:
        username = receive(user)
        if username == "":
            pass
        elif search_user(username, 0)[1]:
            send(user, "Username already taken! Please provide a different username:")
        else:
            user = (username, user_socket, user_addr)
            users.append(user)
            send(user, str("User " + user[0] + " has been registered."))
            validname = True
    return user

def discon_user(user):
    print(user[0] + " disconnected!")
    send(user, "You have been disconnected!")
    user[1].close()
    users.remove(user)
    sys.exit()

def choose_chat_friend(user):
    validfriend = False
    while not validfriend:
        msg_recv = receive(user)
        if msg_recv.lower() == "/disconnect":
            discon_user(user)
            break
        else:
            chat_friend, user_exist = search_user(msg_recv, 0)
            if user_exist == True:
                if user[0] == chat_friend[0]:
                    send(user, "You cannot chat with yourself! Please choose a different friend from the list.")
                else:
                    validfriend = True
                    return chat_friend
            else:
                send(user, "That user could not be found! Please choose a friend from the list.")

def chat_to(user, chat_friend):
    send(user, "You are now chatting to " + chat_friend[0] + '.\nType "/exit" to get to the lobby, or "/disconnect" to disconnect!')
    while True:
        msg = receive(user)
        if msg == "/disconnect":
            discon_user(user)
        elif msg == "/exit":
            return
        else:
            send(chat_friend, msg)

def handle_user(user_socket, user_addr):
    user = new_user(user_socket, user_addr)
    while True:
        lobby_str = str("Welcome to the lobby, " + user[0] + "!\nPlease choose an online friend to chat with from the list below!\n\n" + get_user_list() + '\n\n("/disconnect" to disconnect from server)')
        send(user, lobby_str)
        print(str(user[0] + " has entered the lobby"))
        chat_friend = choose_chat_friend(user) #user chooses a friend to chat to or disconnects
        chat_to(user, chat_friend)

def start():
    SERVER.listen()
    print("[LISTENING] Server is listening on port " + str(PORT) + "!")
    while True:
        conn, addr = SERVER.accept()
        thread = threading.Thread(target=handle_user, args=(conn, addr))
        thread.start()
        print("[CONNECTED] Client on ip " + str(addr[0]) + " has connected to the server!")

start()
