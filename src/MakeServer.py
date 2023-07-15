import datetime, requests, shutil, getpass, json, os
from Javasystem.etc import exec_java

backslash = '\\'

def download_file(url : str, save_name : str, user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"):
    try:
        if "http" in url == False:
            url = "http://"+url
        header = {
            'User-Agent': user_agent
        }
        response = requests.get(url, headers=header)
        if not response.status_code[:1] in [2,3]:
            return False
        with open(save_name ,mode='wb') as f:
            f.write(response.content)
        return True
    except:
        return False

def spigot_download(minecraft_dir, server_version):
    result = None
    if download_file("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar", minecraft_dir+"/Spigot-BuildTools.jar") == False:
        return 1
    try:
        exec_java(f"./{minecraft_dir}", "Spigot-BuildTools.jar", 1, 1, java_argument="-rev "+server_version)
        result = 0
    except Exception as e:
        result = 2
    return result

def install_forge_server(minecraft_dir, server_version, forge_id):
    result = None
    if download_file(f"https://maven.minecraftforge.net/net/minecraftforge/forge/{server_version}-{forge_id}/forge-{server_version}-{forge_id}-installer.jar", f"{minecraft_dir}/forge-{server_version}-{forge_id}-installer.jar")  == False:
        return 1
    try:
        exec_java(minecraft_dir, f"forge-{server_version}-{forge_id}-installer.jar", "1", "1", java_argument="--installServer")
        result = 0
    except:
        result = 2
    return result

def get_minecraft_url(version):
    file = open('data/version.json', 'r')
    json_object = json.load(file)
    minecraft_editions = ["stable", "snapshot"]
    successs = []
    for minecraft_edition in minecraft_editions:
        try:
            minecraft_server_url = json_object[minecraft_edition][version]["server"]
            successs.append(True)
        except KeyError:
            successs.append(False)
    if not successs[0] and not successs[1]:
        return False, "not"
    return True, minecraft_server_url

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

def make(server_name : str, server_port : int , server_version : str, edition : str, message : bool, eula : bool, forge_id = ""):
    start_jar = None
    
    dt_now        = datetime.datetime.now()
    dt_now_utc    = datetime.datetime.now(datetime.timezone.utc)
    minecraft_dir = "minecraft/minecraft-"+dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f')
    absolute_path = os.getcwd().replace("\\", "/")

    os.makedirs("data", exist_ok=True)
    os.makedirs(minecraft_dir, exist_ok=True)

    if message == True:
        print("しばらくお待ち下さい。\n回線の状況によっては時間が長くなる可能性もあります。")
    if download_file("http://mcversions.net/mcversions.json", "data/version.json") == False:
        return 3, ""
    isversion, server_url = get_minecraft_url(server_version)
    if not isversion:
        return 2, ""
    match edition:
        case 'vanilla':
            if download_file(server_url, minecraft_dir+"/server.jar", user_agent="") == False:
                return 3, ""
            start_jar = "server.jar"
        case 'spigot':
            match spigot_download(minecraft_dir, server_version):
                case 0:
                    pass
                case 1:
                    return 3, ""
                case 2:
                    return 4, ""
            start_jar = "server.jar"
        case 'forge':
            match install_forge_server(minecraft_dir, server_version, forge_id):
                case 0:
                    pass
                case 1:
                    return 3, ""
                case 2:
                    return 5, ""
            start_jar = "forge-"+server_version+"-"+forge_id+".jar"
        case _:
            return 1, ""
    
    if download_file("https://server.properties/", minecraft_dir+"/server.properties") == False:
        return 3, ""
    try:
        file_identification_rewriting(minecraft_dir+"/server.properties", "server-port=", "server-port="+str(server_port)+"\n")
        file_identification_rewriting(minecraft_dir+"/server.properties", "motd=", "motd="+server_name+"\n")
        with open(minecraft_dir+"/eula.txt", mode='a') as f:
            f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#"+dt_now_utc.strftime('%a')+" "+dt_now_utc.strftime('%b')+" "+dt_now_utc.strftime('%d')+" "+dt_now_utc.strftime('%H:%M:%S')+" "+str(dt_now_utc.tzinfo)+" "+dt_now_utc.strftime('%Y')+"\neula="+str(eula))
        with open("./data/setting.ini", mode='a') as f:
            f.write(f"[{minecraft_dir.lower()}]\nserver_name = {server_name}\nversion = {server_version}\nstart_jar = {start_jar}\nabsolute_path = {absolute_path}/{minecraft_dir}\nmake_user = {getpass.getuser()}")
        f = open("./data/unsetting.ini", 'a')
        f.write("")
        f.close()

    except:
        return 6, ""
    return 0, minecraft_dir.replace('minecraft/' , '')