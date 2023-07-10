import MakeServer
from TextJudgement import yes_no_text
import requests

def get_http_status_code(url : str):
    r = requests.get(url)
    return r.status_code

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

def make():
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
    MakeServer.make(server_info[0], int(server_info[1]), server_info[2], server_info[4], True, server_info[3], server_info[5])