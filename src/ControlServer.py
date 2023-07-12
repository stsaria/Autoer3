import configparser, os

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
    if not os.path.isfile("./data/setting.ini"):
        return 1
    ini = configparser.ConfigParser()
    ini.read('./data/config.ini', 'UTF-8')
    if list(ini)[1:] < 1:
        return 2
    for i in list(ini)[1:]:
        server_name = ini[i]['server_name']
        version = ini[i]['version']
        start_jar = ini[i]['start_jar']
        servers.append([i, server_name, version, start_jar])
    return 0, list(ini)[1:], servers

def start_server(server_id):
    pass

def change_port(server, port):
    result = server_list()[0]
    if result != 0:
        return result
    if not server in result:
        return 3
    path = f"./{server}"
    if not os.path.isfile(f"{path}/server.properties"):
        return 4
    try:
        file_identification_rewriting(f"{path}/server.properties",
                                            "server-port=", "server-port="+port+"\n")
    except:
        return 5
    return 0
    
    
