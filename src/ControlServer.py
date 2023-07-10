import configparser, os

def start_server(server_id):
    pass

def change_port(server, port):
    """サーバーのポートを再設定する関数"""
    if not os.path.isfile("./data/setting.ini"):
        return 1
    ini = configparser.ConfigParser()
    ini.read('./data/config.ini', 'UTF-8')
    if len(ini) < 1:
        return 2
    if not server in list(ini)[1:]:
        return 3
    path = ini[server][]
    make.file_identification_rewriting(path+"/server.properties",
                                        "server-port=", "server-port="+input_port+"\n")
    print("サーバーのポートを変更しました。")

def server_list():
    if not os.path.isfile("./data/setting.ini"):
        return 1
    ini = configparser.ConfigParser()
    ini.read('./data/config.ini', 'UTF-8')
    if list(ini)[1:] < 1:
        return 2
    return list(ini)[1:]
    
    