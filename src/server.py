import threading, socket, sys
from MakeServer import make
from TextJudgement import true_false_string

def handle_client(client_socket, address):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            server_info = data.split('|')
            if server_info[0] == "m":
                print("aa")
                result = make(server_info[1], server_info[2], server_info[3], server_info[5], False, true_false_string(server_info[4]), server_info[6])
                if result[0] != 0:
                    error_text = ""
                    match result[0]:
                        case 1:
                            error_text = "特定不能のエラーです"
                        case 2:
                            error_text = "特定不能なサーバーバージョンです"
                        case 3:
                            error_text = "サーバーファイルのダウンロードに失敗しました"
                        case 4:
                            error_text = "BuildToolsの実行時にエラーが発生しました"
                        case 5:
                            error_text = "Forgeインストール時にエラーが発生しました"
                        case 6:
                            error_text = "ファイルの書き込み中にエラーが発生しました"
                    client_socket.send(f"ng|{error_text}".encode('utf-8'))
                    client_socket.close()
                    return
                else:
                    client_socket.send(f"ok|{result[1]}".encode('utf-8'))    
                    client_socket.close()
                    return
            break
        client_socket.close()
        return
            #if server_info[0] == "c":
            #    if len(server_info) == 2:
            #        if server_info[1] == "serverlist":

    except Exception as e:
        print(f"エラーが発生しました！：{e}")
        sys.exc_clear()
        client_socket.close()

def main(port = 26696):
    print("終了する際はCtrl+Cで終了してください。")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    try:
        while True:
            client_socket, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()

    except KeyboardInterrupt:
        print("サーバーが終了されます")
        server_socket.close()