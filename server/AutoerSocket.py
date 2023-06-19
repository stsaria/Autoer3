import socket

'''no|false|false|false|false|no|
   mem del   shf   sw   sysd  sn 
   [0] [1]  [2]   [3]   [4]  [5]
   str  bool bool bool  bool str
   int  ---- ---- ----  ---- int'''

HOST = 'localhost'
PORT = 58797

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
client_socket, addr = server_socket.accept()

while True:
    data = client_socket.recv(1024)
    if not data:
        print("ERR!!!!!!!")
        break
    result = data.decode().split('|')
    print('', data.decode())

client_socket.close()
server_socket.close()