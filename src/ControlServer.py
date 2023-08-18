import configparser, subprocess, MakeServer, platform, shutil, socket, etc, os
from PIL import Image

def replace_func(fname, replace_set):
    target, replace = replace_set
    with open(fname, 'r') as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)
    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

def file_identification_rewriting(file_name, before, after):
    replace_setA = (before, after)
    replace_func(file_name, replace_setA)

def server_list():
    servers = []
    server_id = []
    if not os.path.isfile("./data/setting.ini") or not os.path.isfile("./data/unsetting.ini"):
        return 1, server_id, servers
    ini = configparser.ConfigParser()
    ini.read('./data/setting.ini', 'UTF-8')
    unini = configparser.ConfigParser()
    unini.read('./data/unsetting.ini', 'UTF-8')
    server_id = list(ini)[1:]
    if len(server_id) < 1:
        return 2, "server_id", servers
    for i in range(len(server_id)):
        if server_id[i] in list(unini)[1:]:
            server_id.remove(server_id[i])
    for i in server_id:
        server_name = ini[i]['server_name']
        version = ini[i]['version']
        start_jar = ini[i]['start_jar']
        absolute_path = ini[i]['absolute_path']
        make_user = ini[i]['make_user']
        servers.append([i.replace('minecraft/', ''), server_name, version, start_jar, absolute_path, make_user])
    return 0, server_id, servers

def edit_server(server_id, use_editer = ""):
    identification_server = None
    file = ""
    result = server_list()
    user_use_platfrom = platform.system()
    if result[0] != 0:
        return result[0]
    for i in range(len(result[2])):
        if server_id == result[2][i][0]:
            identification_server = i
    if identification_server == None:
        return 1
    else:
        path = result[2][int(str(identification_server))][4]
    if "minecraft" in server_id:
        file = "server.properties"
    elif "bungeecord" in server_id:
        file = "config.yml"
    try:
        if user_use_platfrom == "Windows":
            subprocess.run(f"notepad.exe {file}", shell=True, cwd=f"{path}/", check=True)
        else:
            print(f"{use_editer} {file}")
            subprocess.run(f"{use_editer} {file}", shell=True, cwd=f"{path}/", check=True)
    except Exception as e:
        print(e)
        return 2
    return 0

def start_server(server_id, xms = 1, xmx = 1):
    identification_server = None
    result = server_list()
    if result[0] != 0:
        return result[0]
    for i in range(len(result[2])):
        if server_id == result[2][i][0]:
            identification_server = i
    if identification_server == None:
        return 3
    else:
        path = result[2][int(str(identification_server))][4]
    if int(xms) < 1 or int(xmx) < 1:
        return 4
    try:
        subprocess.run(f"java -Xmx{xmx}G -Xms{xms}G -jar {result[2][int(str(identification_server))][3]} nogui", shell=True, cwd=f"{path}/", check=True)
    except Exception as e:
        return 5
    except KeyboardInterrupt:
        pass
    return 0

def add_startup(server_id, start_autoer_program, xms = 1, xmx = 1, systemd_mode = 0):
    absolute_path = os.getcwd().replace("\\", "/")
    if "Autoer.py" in  start_autoer_program:
        start_command = f"python -u {start_autoer_program} -r {server_id} {xms} {xmx}"
    else:
        start_command = f"{start_autoer_program} -r {server_id} {xms} {xmx}"
    identification_server = None
    if etc.is_admin() == False:
        return 3
    user_use_platfrom = platform.system()
    result = server_list()
    if result[0] != 0:
        return result[0]
    for i in range(len(result[2])):
        if server_id == result[2][i][0]:
            identification_server = i
    if identification_server == None:
        return 4
    if int(xms) < 1 or int(xmx) < 1:
        return 5
    try:
        if user_use_platfrom == "Windows":
            file = open(f"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/{server_id}.bat", mode='w')
            file.write(f"cd {absolute_path}\n\
                        {start_command}\n\
                        pause")
            file.close()
        else:
            if not shutil.which('systemctl'):
                return 6
            exec_start = f"/usr/bin/env {start_command}"
            if systemd_mode == 1:
                if not shutil.which('screen'):
                    return 6
                exec_start = f"/usr/bin/screen -DmS {server_id} /usr/bin/env {start_command.replace('python', 'python3')}"
            file = open(f"/etc/systemd/system/{server_id}.service", mode='w')
            file.write(f"[Unit] \
            \nDescription=Minecraft Server: %i \
            \nAfter=network.target \
            \n[Service] \
            \nWorkingDirectory={absolute_path} \
            \nUser={result[2][int(str(identification_server))][5]}\
            \nRestart=always \
            \nExecStart={exec_start}\
            \n[Install] \
            \nWantedBy=multi-user.target")
            file.close()
            subprocess.run("systemctl daemon-reload", shell=True, check=True)
            subprocess.run(f"systemctl enable {server_id}.service", shell=True, check=True)
    except:
        return 6
    return 0

def del_startup(server_id):
    identification_server = None
    if etc.is_admin() == False:
        return 3
    user_use_platfrom = platform.system()
    result = server_list()
    if result[0] != 0:
        return result[0]
    for i in range(len(result[2])):
        if server_id == result[2][i][0]:
            identification_server = i
    if identification_server == None:
        return 4
    if os.path.isfile(f"/etc/systemd/system/{server_id}.service") or os.path.isfile(f"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/{server_id}.bat"):
        try:
            if user_use_platfrom == "Windows":
                os.remove(f"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/{server_id}.bat")
            elif user_use_platfrom == "Linux":
                if not shutil.which('systemctl'):
                    return 6
                os.remove(f"/etc/systemd/system/{server_id}.service")
                subprocess.run("systemctl daemon-reload", shell=True, check=True)
        except:
            return 6
    else:
        return 5
    return 0

def del_server(server_id):
    result = server_list()
    absolute_path = os.getcwd().replace("\\", "/")
    identification_server = None

    if result[0] != 0:
        return result[0]
    for i in range(len(result[2])):
        if server_id == result[2][i][0]:
            identification_server = i
    if identification_server == None:
        return 3
    else:
        path = result[2][int(str(identification_server))][4]
    try:
        with open("./data/unsetting.ini", mode='a') as f:
            f.write(f"[minecraft/{result[2][int(str(identification_server))][0]}]\nserver_name = {result[2][int(str(identification_server))][1]}\nversion = {result[2][int(str(identification_server))][2]}\nabsolute_path = {absolute_path}/minecraft/{result[2][int(str(identification_server))][0].lower()}\n")
        shutil.rmtree(path)
    except Exception as e:
        return 4
    return 0

def change_port(server_id : str, port : int):
    result = server_list()
    identification_server = None

    if "bungeecord" in server_id:
        return 3

    if result[0] != 0:
        return result[0]
    for i in range(len(result[2])):
        if server_id == result[2][i][0]:
            identification_server = i
    if identification_server == None:
        return 3
    else:
        path = result[2][int(str(identification_server))][4]
    if not os.path.isfile(f"{path}/server.properties"):
        return 4
    try:
        file_identification_rewriting(f"{path}/server.properties",
                                            "server-port=", "server-port="+str(port)+"\n")
    except Exception as e:
        print(e)
        return 5
    return 0
    
def transfer_server(servers : list, is_minimum : bool, is_unsupported : bool):
    identification_server = [None, None]
    path = [None, None]
    required_copy_dir_and_file = ["world", "world_nether", "world_the_end", "server.properties", "banned-players.json", "banned-ips.json", "whitelist.json", "ops.json", "eula.txt"]
    optional_copy_dir_and_file = ["server-icon.png", "spigot.yml", "plugins", "mods"]
    result = server_list()
    for i in range(len(servers)):
        if result[0] != 0:
            return result[0]
        for j in range(len(result[2])):
            if servers[i] == result[2][j][0]:
                identification_server[i] = j
        if identification_server[i] == None:
            if is_unsupported == True:
                if os.path.isdir(servers[i]):
                    path[i] = servers[i]
                else:
                    return 3
            else:
                return 3
        else:
            path[i] = result[2][int(str(identification_server[i]))][4]
    try:
        if "minecraft" in servers[0] and "minecraft" in servers[1]:
            for i in required_copy_dir_and_file:
                if os.path.isfile(f"{path[0]}/{i}"):
                    shutil.copy2(f"{path[0]}/{i}", path[1])
                elif os.path.isdir(f"{path[0]}/{i}"):
                    if os.path.isdir(f"{path[1]}/{i}"):
                        shutil.rmtree(f"{path[1]}/{i}")
                    shutil.copytree(f"{path[0]}/{i}", f"{path[1]}/{i}")
                else:
                    continue
                print(f"{path[0]}/{i} -> {path[1]}/{i}")
            if is_minimum != True:
                for i in optional_copy_dir_and_file:
                    if os.path.isfile(f"{path[0]}/{i}"):
                        shutil.copy2(f"{path[0]}/{i}", path[1])
                    elif os.path.isdir(f"{path[0]}/{i}"):
                        if os.path.isdir(f"{path[1]}/{i}"):
                            shutil.rmtree(f"{path[1]}/{i}")
                        shutil.copytree(f"{path[0]}/{i}", f"{path[1]}/{i}")
                    else:
                        continue
                    print(f"{path[0]}/{i} -> {path[1]}/{i}")
        elif "bungeecord" in servers[0] and "bungeecord" in servers[1]:
            if os.path.isfile(f"{path[0]}/config.yml"):
                shutil.copy2(f"{path[0]}/config.yml", path[1])
    except Exception as e:
        return 4
    return 0

def make_html(path = "./"):
    readme_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>マニュアル</title>
</head>
<body>
    <h1>Autoer3</h1>
    <h2>Autoer3とAutoerとは</h2>
    <p>
        Autoer3とはAutoer系統のプログラムです
        <br/>Autoerはマイクラを半自動作成するプログラムです
    </p>

    <h2>条件</h2>
    <p>
        1.ネットワーク環境がある
        <br/>2.Python3.10以上
        <br/>3.requestsがインストールされてる
        <br/> ※実行ファイルの場合はインストール不要
    </p>
    
    <h2>導入</h2>
    <p>
        1.Releaseからソースコードをダウンロードします
        <br/>※実行ファイルでも問題ないです
        <br/>2.Pythonのrequestsをダウンロードします
        <br/><span style="background-color : black; color : white; width : fit-content;">$ pip install requests</span>
        <br/>3.Autoerを実行します
        <br/><span style="background-color : black; color : white; width : fit-content;">$ python src/Autoer.py</span>
        <br/>もしくは
        <br/><span style="background-color : black; color : white; width : fit-content;">$ ./Autoer</span>
        <br/>次のように引数を与えずに実行すると引数の与え方の説明が出ます
    </p>

    <h2>注意</h2>
    <p>
        ・このプログラムを不正に使わないでください
    </p>

    <h2>引数の使い方</h2>
    <span style="background-color : black; color : white; width : fit-content;">Autoer -[s,m,bs,bm,R,r,cp,sl,sysdm,sysdr,se,trans,legacy-trans] [etc_args]</span>
                <h3>引数欄:</h3>
                    <h4>起動モード:</h4>
                        <p>
                            -s,-m : 作成
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-m [server_name (スペース, タブなし)] [server_port (1~65535)] [server_version (プレリリース版でも可※)] [eula (true or false)] [server_edition (vanilla, spigot, forge, paper)] [build_id (Forge※, PaperMC※ 使用時のみ)]</span>)
                            <br/>※プレリリース版はForge, PaperMCとの組み合わせでは使えません
                            <br/>※ForgeはBuildIDの取得ができません
                            <br/>※PaperMCはBuildIDを省略すれば自動的に新しいjarファイルがダウンロードされます
                            <br/>
                            <br/>-bs,-bm : Bungeecordの作成
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-bm [server_name (スペース, タブなし)] [server_port (1~65535)]</span>)
                            <br/>
                            <br/>-auto 限りなく自動に近いサーバー作成<br/>
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-auto [server_name (スペース, タブなし)] [eula (true or false)]</span>)
                            <br/>上記以外はこちらで作成されます
                            <br/>Version : 最新
                            <br/>Port : 25565
                            <br/>Edithon : Vanilla
                            <br/>管理者の場合は自動起動設定を実行します
                            <br/>
                            <br/>-R : 削除
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-R [server_id]</span>)
                            <br/>
                            <br/>-r : 起動
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-r [server_id] [Xms (int)(最小メモリ)] [Xmx (int)(最大メモリ)]</span>)
                            <br/>
                            <br/>-sl : サーバーリストの表示
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-sl</span>)
                            <br/>
                            <br/>-cp : サーバーのポート変更
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-cp [server_id] [server_new_port (1~65535)]</span>)
                            <br/>
                            <br/>-sysdm,-sysds サーバーをSystemd Deamon,スタートアップに登録する(自動起動設定)(※管理者権限が必須です)
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-sysdm [server_id] [Xms (int)(最小メモリ)] [Xmx (int)(最大メモリ)] -screen (Screenでの起動(Windows以外))</span>)
                            <br/>
                            <br/>-sysdr サーバーのSystemd Deamon,スタートアップを削除する(自動起動解除)(※管理者権限が必須です)
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-sysdr [server_id]</span>)
                            <br/>
                            <br/>-se サーバー管理ファイルの編集モード(Minecraftでserver.propeties、Bungeecordでconfig.yml)
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-se [server_id] [editer(Windows以外)]</span>)
                            <br/>
                            <br/>-trans サーバーの情報を移行するモード(Minecraftでworld, world_nether, world_the_end, server.properties, spigot.yml(Spigot, Paperのみ)、Bungeecordでconfig.yml)
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-trans [before_server_id (移行元のサーバー)] [after_server_id (移行先のサーバー)] -minimum (必要最低限のファイル)</span>)
                            <br/>
                            <br/>-unsupported-trans Autoerではないサーバーを-transのように移行できるモード
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-unsupported-trans [before_server_id_or_dir (移行元のサーバー)] [after_server_or_id (移行先のサーバー)] -minimum (必要最低限のファイル)</span>)
                            <br/>
                            <br/>-html, -reload-html サーバー一覧をHTMLに出力するモード
                            <br/>(方法 : <span style="background-color : black; color : white; width : fit-content;">-html [path(任意)]</span>)
                            <br/>
                            <br/>※server_id は サーバー作成時に発行されたID(-sl(サーバーリスト表示)でIDを確認することができます)
                        </p>
    <a href="../index.html"><p style="float : left">ホームに戻る</p></a>
</body>
</html>"""
    
    result = server_list()
    hostname = socket.gethostname()
    if result[0] != 0:
        return result[0]
    try:
        os.makedirs(path+"/servers", exist_ok=True)
        os.makedirs(path+"/manual", exist_ok=True)
        with open(f"{path}/manual/readme.html", mode='w', encoding='utf-8') as f:
            f.write(readme_html)
        for i in result[2]:
            ico = "https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/favicon.ico"
            png = "https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/apple-icon-72x72.png"
            if os.path.isfile(f"{i[4]}/server-icon.png"):
                png = f"{i[4]}/server-icon.png"
                ico = f"{i[4]}/server-icon.ico"
                img = Image.open(png)
                img.save(ico, format="ICO", sizes=[(64, 64)])
            
            server_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/x-icon" sizes="64x64" href="{ico}">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{i[0]}</title>
</head>
<body>
    <img src="{png}" width="64" height="64" style="float : left"/><h1>{i[0]}</h1>
    <p>サーバーID : {i[0]}</br>
    サーバー名 : {i[1]}</br>
    サーバーバージョン : {i[2]}</br>
    サーバーの場所(パス) : {i[4]}
    </p>
    <div>
    <span style="float : left">・サーバーの起動方法&ensp;</span><span style="background-color : black; color : white; width : fit-content; float : left;">$ ./Autoer -r {i[0]} Xms Xmx</span>
    </div>
    </br>
    <div>
    <span style="float : left">・サーバーの削除方法&ensp;</span><span style="background-color : black; color : white; width : fit-content; float : left;">$ ./Autoer -R {i[0]} Xms Xmx</span>
    </div>
    </br>
    <a href="../index.html"><p style="float : left">ホームに戻る</p></a>
</body>
</html>"""
            with open(f"{path}/servers/{i[0]}.html", mode='w', encoding='utf-8') as f:
                f.write(server_html)

        index_server_list_html = ""
        for i in result[2]:
            index_server_list_html = f"""{index_server_list_html}<a href="servers/{i[0]}.html"><p>・サーバーID : {i[0]} サーバー名 : {i[1]}</p></a>\n    """
        index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{hostname}のAutoer</title>
</head>
<body>
    <h1>{hostname}のAutoer3</h1>
    <h2>サーバー一覧</h2>
    {index_server_list_html}
    <br/>
    <a href="manual/readme.html"><h3>マニュアル</h3></a>
</body>
</html>"""
        with open(f"{path}/index.html", mode='w', encoding='utf-8') as f:
            f.write(index_html)
    except Exception as e:
        print(e)
        return 3
    return 0