import MakeServer, ControlServer, platform, requests, socket, sys
from TextJudgement import yes_no_text, true_false_string
from Javasystem import check

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
    result = MakeServer.make(server_info[0], int(server_info[1]), server_info[2], server_info[4], True, server_info[3], server_info[5])
    return result

def main(args : list):
    if len(args) == 1:
        args_list_message = """
        Autoer -[s,m,bs,bm,R,r,cp,sl,sysdm,sysdr,se] [etc_args]
        引数欄:
            起動モード:
                -s,-m : 作成
                (方法 : -m [server_name(スペース, タブなし)] [server_port(1~65535)] [server_version] [eula(true or false)] [server_edition(vanilla, spigot, forge, paper)] [build_id(Forge, PaperMC使用時のみ)])

                -bs,-bm : Bungeecordの作成
                (方法 : -bm [server_name(スペース, タブなし)] [server_port(1~65535)])
                
                -R : 削除
                (方法 : -R [server_id (サーバー作成時に発行されたID(-S(サーバーリスト表示)でIDを確認することができます))])

                -r : 起動
                (方法 : -r [server_id (サーバー作成時に発行されたID(-S(サーバーリスト表示)でIDを確認することができます))] [Xms(int)(最小メモリ)] [Xmx(int)(最大メモリ)])

                -sl : サーバーリストの表示
                (方法 : -sl)
                
                -cp : サーバーのポート変更
                (方法 : -c [server_id (サーバー作成時に発行されたID(-S(サーバーリスト表示)でIDを確認することができます))] [server_new_port(1~65535)])

                -sysdm,-sysds サーバーをSystemd Deamon,スタートアップに登録する(自動起動設定)(※管理者権限が必須です)
                (方法 : -sysdm [server_id (サーバー作成時に発行されたID(-S(サーバーリスト表示)でIDを確認することができます))] [Xms(int)(最小メモリ)] [Xmx(int)(最大メモリ)])

                -sysdr サーバーのSystemd Deamon,スタートアップを削除する(自動起動設定)(※管理者権限が必須です)
                (方法 : -sysdr [server_id (サーバー作成時に発行されたID(-S(サーバーリスト表示)でIDを確認することができます))])

                -se サーバー管理ファイルの編集モード(Minecraftでserver.propeties, Bungeecordでconfig.yml)
                (方法 : -se [server_id (サーバー作成時に発行されたID(-S(サーバーリスト表示)でIDを確認することができます))] [editer(Windows以外)])
        """
        print(args_list_message)
    for i in range(5):
        args.append("")
    else:
        if check.java_version()[0] == False:
            print("Javaがインストールされていません")
            return 7

        if args[1] == "-s" or args[1] == "-m":
            result = ""
            if len(args) - 2 >= 5:
                build_id = ""
                if len(args) - 2 >= 6:
                    build_id = args[7]
                if not str(args[3]).isdigit():
                    print("入力フォーマットが間違っています")
                    return 7
                max_port = 6000
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                return_code = sock.connect_ex(("127.0.0.1", int(args[3])))
                sock.close()
                if return_code == 0:
                    print("警告 : このポートは使用されています")
                try:
                    result = MakeServer.make(str(args[2]), int(str(args[3])), str(args[4]), str(args[6]), True, true_false_string(str(args[5])), str(build_id))
                except InterruptedError:
                    print("入力フォーマットが間違っています")
                    return 7
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
                print(f"サーバーの作成に失敗しました\n{error_text}")
                return result[0]
            else:
                print(f"サーバーの作成に成功しました\n作成したサーバーID : {result[1]}")
                return 0
        if args[1] == "-bm" or args[1] == "-bs":
            result = ""
            if len(args) - 2 >= 2:
                if not str(args[3]).isdigit():
                    print("入力フォーマットが間違っています")
                    return 7
                max_port = 6000
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                return_code = sock.connect_ex(("127.0.0.1", int(args[3])))
                sock.close()
                if return_code == 0:
                    print("警告 : このポートは使用されています")
                result = MakeServer.install_bungeecord_server(str(args[2]), int(str(args[3])))
                if result[0] != 0:
                    error_text = ""
                    match result[0]:
                        case 1:
                            error_text = "サーバーファイルのダウンロードに失敗しました"
                        case 2:
                            error_text = "ファイルの書き込み中にエラーが発生しました"
                    print(f"サーバーの作成に失敗しました\n{error_text}")
                    return result[0]
                else:
                    print(f"サーバーの作成に成功しました\n作成したサーバーID : {result[1]}")
                    return 0
        if args[1] == "-se":
            result = ""
            editer = ""
            if len(args) - 2 >= 1:
                if len(args) - 2 >= 2:
                    editer = str(args[3])
                result = ControlServer.edit_server(str(args[2]), editer)
                if result != 0:
                    error_text = ""
                    match result:
                        case 1:
                            error_text = "サーバーが見つかりませんでした"
                        case 2:
                            error_text = "ファイルの書き込みに失敗しました"
                    print(f"サーバーファイルの編集に失敗しました\n{error_text}")
                    return result
                else:
                    print(f"サーバーファイルの編集が終了しました")
                    return 0

        if args[1] == "-R":
            result = ControlServer.del_server(str(args[2]))
            if result != 0:
                error_text = ""
                match result:
                    case 1:
                        error_text = "特定不能のエラーです"
                    case 2:
                        error_text = "特定不能なサーバーバージョンです"
                    case 3:
                        error_text = "指定したサーバーがありません"
                    case 4:
                        error_text = "サーバー削除中にエラーが発生しました"
                print(f"サーバーの削除に失敗しました\n{error_text}")
                return result
            else:
                print("サーバーの削除に成功しました")
                return 0
        if args[1] == "-cp":
            result = ""
            if len(args) >= 4:
                if not str(args[3]).isdigit():
                    print("入力フォーマットが間違っています")
                    return 7
                result = ControlServer.change_port(args[2], int(args[3]))
                if result != 0:
                    error_text = ""
                    match result:
                        case 1:
                            error_text = "サーバーの管理ファイルが存在しません\n※ディレクトリはのターゲットは作成時と同じである必要があります\n※ディレクトリを指定したい場合は-pathをつけて実行してください"
                        case 2:
                            error_text = "サーバーの管理ファイルの中身が空です\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                        case 3:
                            error_text = "指定したサーバーがありません"
                        case 4:
                            error_text = "サーバー設定ファイル(server.properties)が存在しません\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                        case 5:
                            error_text = "ファイルの書き込み中にエラーが発生しました"
                        case 6:
                            error_text = "ポートの番号が範囲外です\n※ポート番号は1~65535までです"
                    print("ポートの変更に失敗しました\n"+error_text)
                    return result
                else:
                    print("ポートの変更に成功しました")
                    return 0
        if args[1] == "-sysdm" or args[1] == "-sysds":
            result = ""
            systemd_mode = 0
            if len(args) >= 5:
                if not str(args[3]).isdigit() or not str(args[4]).isdigit():
                    print("入力フォーマットが間違っています")
                    return 7
                if len(args) >= 6:
                    if args[5] == "-screen":
                        systemd_mode = 1
                result = ControlServer.add_startup(args[2], args[0], int(args[3]), int(args[4]), systemd_mode)
                if result != 0:
                    error_text = ""
                    match result:
                        case 1:
                            error_text = "サーバーの管理ファイルが存在しません\n※ディレクトリはのターゲットは作成時と同じである必要があります\n※ディレクトリを指定したい場合は-pathをつけて実行してください"
                        case 2:
                            error_text = "サーバーの管理ファイルの中身が空です\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                        case 3:
                            error_text = "管理者で実行されていません"
                        case 4:
                            error_text = "指定したサーバーがありません"
                        case 5:
                            error_text = "メモリが1GBより少ないです"
                        case 6:
                            error_text = "自動起動設定中にエラーが発生しました"
                    print("自動起動設定に失敗しました\n"+error_text)
                    return result
                else:
                    print("自動起動設定に成功しました\n※まだ起動していませんのでご注意ください")
                    if not platform.system() == "Windows":
                        print(f"立ち上げ : systemctl start {args[2]}\n終了 : systemctl stop {args[2]}\n動作状況表示 : systemctl status {args[2]}")
                        if systemd_mode == 1:
                            print(f"マイクラのコンソールを表示するときは以下のコマンドをお使いください\nscreen -r {args[2]}\n終了する際はCtrl+A+Dです")
                    return 0
        if args[1] == "-sysdr":
            result = ""
            if len(args) >= 3:
                result = ControlServer.del_startup(args[2])
                if result != 0:
                    error_text = ""
                    match result:
                        case 1:
                            error_text = "サーバーの管理ファイルが存在しません\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                        case 2:
                            error_text = "サーバーの管理ファイルの中身が空です\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                        case 3:
                            error_text = "管理者で実行されていません"
                        case 4:
                            error_text = "指定したサーバーがありません"
                        case 5:
                            error_text = "指定したサーバーは自動起動設定されていません"
                        case 6:
                            error_text = "自動起動解除中にエラーが発生しました"
                    print("自動起動解除に失敗しました\n"+error_text)
                    return result
                else:
                    print("自動起動解除に成功しました")
                    return 0
        if args[1] == "-sl":
            result = ""
            result = ControlServer.server_list()
            if result[0] != 0:
                error_text = ""
                match result:
                    case 1:
                        error_text = "サーバーの管理ファイルが存在しません\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                    case 2:
                        error_text = "サーバーの管理ファイルの中身が空です\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                print("サーバーリストの取得に失敗しました")
                return result[0]
            else:
                for i in result[2]:
                    print(f"サーバーID : {i[0]}", f"サーバー名 : {i[1].replace('minecraft/', '')}", f"サーバーバージョン : {i[2]}")
        if args[1] == "-r":
            result = ""
            if len(args) >= 5:
                if not str(args[3]).isdigit() or not str(args[4]).isdigit():
                    print("入力フォーマットが間違っています")
                    return 7
                result = ControlServer.start_server(args[2], int(args[3]), int(args[4]))
                if result != 0:
                    error_text = ""
                    match result:
                        case 1:
                            error_text = "サーバーの管理ファイルが存在しません\n※ディレクトリはのターゲットは作成時と同じである必要があります\n※ディレクトリを指定したい場合は-pathをつけて実行してください"
                        case 2:
                            error_text = "サーバーの管理ファイルの中身が空です\n※ディレクトリはのターゲットは作成時と同じである必要があります"
                        case 3:
                            error_text = "指定したサーバーがありません"
                        case 4:
                            error_text = "メモリが1GBより少ないです"
                        case 5:
                            error_text = "マイクラサーバー動作中にエラーが発生しました"
                    print("マイクラサーバーが異常終了しました\n"+error_text)
                    return result
                else:
                    print("マイクラサーバーが正常終了しました")
                    return 0

if __name__ == "__main__":
    main(sys.argv)
