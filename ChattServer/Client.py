import socket
import threading
server_ip = "127.0.0.1"
server_port = 5050
server_addr = (server_ip, server_port)
HEADER = 10
FORMAT = "utf-8"

def receive():
    while True:
        msg_len = client.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            print(str(client.recv(msg_len).decode(FORMAT)))


def send():
    while True:
        msg_byte = input().encode(FORMAT)
        msg_len = len(msg_byte)
        msg_len_byte = str(msg_len).encode(FORMAT)
        msg_len_byte += b" "*(HEADER - len(msg_len_byte))
        client.send(msg_len_byte)
        client.send(msg_byte)

recvThread = threading.Thread(target=receive)
sendThread = threading.Thread(target=send)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)
recvThread.start()
sendThread.start()

