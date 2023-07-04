import socket, sys
from TextJudgement import yes_no_text, inside_text
from HttpCheckEtc import get_http_status_code

PORT = 26696

def select_number(text : str, choices : list, return_text = []):
    if len(choices) < 1:
        return None
    print(f"{text}\n")
    while True:
        for i in range(len(choices)):
            print(f"{choices[i]} [{str(i+1)}]")
        select = input(f"\n選択してください [1~{str(len(choices))}] : ")
        print()
        if not select.isdigit():
            continue
        elif not 1<=int(select)<=len(choices):
            continue

        if len(choices) == len(return_text):
            return return_text[int(select)-1]
        else:
            return int(select)

def socket_send(host : str, text : str):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, PORT))
        client_socket.send(text.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        if response:
            return response
        client_socket.close()
    except socket.error as e:
        print("作成に失敗しました。")
        return None

def make(server_host : str):
    server_info = [None, None, None, None, None, ""]
    messeges = ["サーバー名を入力してください : ", "ポート番号を入力してください : ", "バージョンを入力してください : ", "Eulaに同意しますか？(詳しくは https://www.minecraft.net/eula をご確認ください) Y[Yes], N[No] : ", "サーバーの種類を選択してください V[Vanilla] (公式サーバー) , S[SpigotMC] , F[Forge] (Mod) : "]
    #
    for i in range(len(server_info[0:5])):
        while True:
            if i == 4:
                server_info[i] = select_number("サーバーの種類を選択してください", ["Vanilla(公式サーバー)", "Spigot(プラグインサーバー)", "Forge(Modサーバー)"], ["vanilla", "spigot", "forge"])
            else:
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
                if server_info[i] in "forge":
                    while True:
                        server_info[i+1] = input("Forgeのビルド番号を入力してください : ")
                        if not 200 <= get_http_status_code("https://maven.minecraftforge.net/net/minecraftforge/forge/"+server_info[2]+"-"+server_info[len(server_info)-1]+"/forge"+server_info[2]+"-"+server_info[len(server_info)-1]+"-installer.jar") < 300:
                            continue
                        break
            break
    format_result = "m|"
    for i in server_info:
        format_result = format_result + str(i) + "|"
    result = socket_send(server_host, format_result)
    if result == None:
        print("作成に失敗しました。")
    if "ok" in result:
        print("作成しました\n作成したサーバーID : "+result.split('|')[1])
    if "ng" in result:
        print("作成に失敗しました\n"+result.split('|')[1])

def control(server_host : str):
    server_info = [None, None, None, None, None, ""]

    select = select_number("管理モードを選択してください", ["サーバー起動モード(※サーバー側はLinuxである必要がある)", "サーバーポート変更モード", "ネットワークの情報確認モード", "スタートアップ(Windows)、Systemd(*Linux)での自動起動の設定モード", "スタートアップ(Windows)、Systemd(*Linux)での自動起動の解除モード"])
    socket_send(server_host, "c|serverlist")    




def main():
    server_host = input("接続先サーバーのホスト名を入力してください (例:192.168.1.25) : ")
    while True:
        select = select_number("モードを選択してください", ["作成", "管理", "終了"], ["make", "control", "exit"])
        if select == "make":
            make(server_host)
        if select == "control":
            pass
        if select == "exit":
            sys.exit(0)

