import socket

def send_text(host : str, port : int, text : str):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("サーバーに接続します。")
        client_socket.send(text.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print("送信しました")
        client_socket.close()
    except Exception as e:
        return False
    return True
if __name__ == '__main__':
    if send_text() == False:
        
