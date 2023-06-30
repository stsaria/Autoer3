import socket, sys
from UiJudgement import yes_no_text, inside_text
from HttpCheckEtc import get_http_status_code

PORT = 26696

def server_create(host : str, text : str):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, PORT))
        print("サーバーに接続します。")
        client_socket.send(text.encode('utf-8'))
        print("送信しました (現在作成中です。プログラムを中断しないでください！！)")
        response = client_socket.recv(1024).decode('utf-8')
        if response == "ok":
            print("作成しました")
        if response == "ng":
            print("作成に失敗しました")
        client_socket.close()
    except Exception:
        print("作成に失敗しました")
        return False
    return True

# 42 is Answers to the Ultimate Questions About Life, the Universe, and Everything

def input_server_info():
    server_info = [None, None, None, None, None, None]
    messeges = ["サーバー名を入力してください : ", "ポート番号を入力してください : ", "バージョンを入力してください : ", "Eulaに同意しますか？(詳しくは https://www.minecraft.net/eula をご確認ください) Y[Yes], N[No] : ", "サーバーの種類を選択してください V[Vanilla] (公式サーバー) , S[SpigotMC] , F[Forge] (Mod) : "]
    #
    for i in range(len(server_info[0:5])):
        while True:
            server_info[i] = None
            server_info[i] = input(messeges[i])
            if i == 1:
                if str(server_info[i]).isdigit():
                    server_info[i] = int(server_info[i])
                else:
                    continue
            elif i == 3:
                try:
                    result = yes_no_text(server_info[i].lower())
                    server_info[i] = None
                    server_info[i] = result
                except InterruptedError:
                    continue
            elif i == 4:
                server_info[i] = server_info[i].lower()
                if server_info[i] in "vanilla":
                    pass
                elif server_info[i] in "spigot":
                    pass
                elif server_info[i] in "forge":
                    server_info[i+1] = input("Forgeのビルド番号を入力してください : ")
                    if not 200 <= get_http_status_code("https://maven.minecraftforge.net/net/minecraftforge/forge/"+server_info[2]+"-"+server_info[len(server_info)-1]+"/forge"+server_info[2]+"-"+server_info[len(server_info)-1]+"-installer.jar") < 300:
                        continue
                else:
                    continue
            break
    if server_info[len(server_info)-1] == None:
        server_info[len(server_info)-1] = "6.6.66.66.6.6"
    return server_info

def main(args = ["42"]):
    server_host = input("接続先サーバーのホスト名を入力してください (例:192.168.1.25) : ")
    result = input_server_info()
    format_result = ""
    for i in result:
        format_result = format_result + str(result) + "|"
    server_create(server_host, format_result)

if __name__ == "__main__":
    main(sys.argv)

