import configparser, subprocess, platform, shutil,  os, etc

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
    if not os.path.isfile("./data/setting.ini") or not os.path.isfile("./data/unsetting.ini"):
        return 1, "server_id", servers
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
        path = f"{result[2][int(str(identification_server))][4]}"
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
        path = f"{result[2][int(str(identification_server))][4]}"
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
    else:
        path = f"{result[2][int(str(identification_server))][4]}"
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
            subprocess.run(f"systemctl enable /etc/systemd/system/{server_id}.service", shell=True, check=True)
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
    else:
        path = f"{result[2][int(str(identification_server))][4]}"
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
        path = f"{result[2][int(str(identification_server))][4]}"
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
        path = f"{result[2][int(str(identification_server))][4]}"
        print(path)
    if not os.path.isfile(f"{path}/server.properties"):
        return 4
    try:
        file_identification_rewriting(f"{path}/server.properties",
                                            "server-port=", "server-port="+str(port)+"\n")
    except Exception as e:
        print(e)
        return 5
    return 0
    
    
