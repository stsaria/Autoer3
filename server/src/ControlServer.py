
import configparser, os

def start_server(server_id):
    pass

def server_list():
    if not os.path.isfile("./data/setting.ini"):
        return 1
    ini = configparser.ConfigParser()
    ini.read('./config.ini', 'UTF-8')
    if len(ini) < 1:
        return 2
    
    