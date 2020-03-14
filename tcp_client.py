from socket import *

sockfd = socket(AF_INET,SOCK_STREAM)

server_addr = ('127.0.0.1',8888)

sockfd.connect(server_addr)

while True:

    data = input('发送：')
    if not data:
        break
    sockfd.send(data.encode())
    data = sockfd.recv(1024)
    print('接受到：',data.decode())


sockfd.close()