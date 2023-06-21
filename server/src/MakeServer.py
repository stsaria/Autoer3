import datetime, requests, shutil, json, os
from Javasystem.etc import exec_java

def download_file(url : str, save_name : str, user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"):
    if "http" in url == False:
        url = "http://"+url
    header = {
        'User-Agent': user_agent
    }
    response = requests.get(url, headers=header)
    print(response.status_code)

    with open(save_name ,mode='wb') as f:
        f.write(response.content)

def spigot_download(minecraft_dir, server_version):
    result = False
    download_file("https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar", minecraft_dir+"/Spigot-BuildTools.jar")
    exec_java("./", "Spigot-BuildTools.jar", "1", "1", java_argument="-rev "+server_version)
    if os.path.isfile("./BuildTools.log.txt"):
        file_readlines = open("./BuildTools.log.txt", 'r').readlines()
        for i in file_readlines[-5:]:
            if "success" in i.lower():
                result = True
                break
    if result == True:
        remove_files = ["Spigot", "CraftBukkit", "work", "Bukkit", "BuildData", "apache-maven-3.6.0"]
        for remove_file in remove_files:
            shutil.rmtree("./"+remove_file)
    return result

def install_forge_server(minecraft_dir, server_version, forge_id):
    result = False
    jar_installer_file = server_version+"-"+forge_id+"/forge-"+server_version+"-"+forge_id+"-installer.jar"
    download_file("https://maven.minecraftforge.net/net/minecraftforge/forge/"+server_version+"-"+forge_id+"/forge-"+server_version+"-"+forge_id+"-installer.jar", minecraft_dir+"/forge-"+server_version+"-"+forge_id+"-installer.jar")
    exec_java(minecraft_dir, "forge-"+server_version+"-"+forge_id+"-installer.jar", "1", "1", java_argument="--installServer")
    if os.path.isfile(minecraft_dir+"/installer.log"):
        file_readlines = open(minecraft_dir+"/installer.log", 'r').readlines()
        for i in file_readlines[-5:]:
            if "success" in i:
                result = True
                break
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

def make(server_name : str, server_port : int , server_version : str, edition : str, forge_id : str, message : bool, eula : bool):
    start_jar = None
    
    dt_now        = datetime.datetime.now()
    dt_now_utc    = datetime.datetime.now(datetime.timezone.utc)
    minecraft_dir = "minecraft/minecraft-"+dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f')

    os.makedirs("data", exist_ok=True)
    os.makedirs(minecraft_dir, exist_ok=True)
    file = open('data/setting.ini','a+')
    file.close()
    if message == True:
        print("しばらくお待ち下さい。\n回線の状況によっては時間が長くなる可能性もあります。")
    download_file("http://mcversions.net/mcversions.json", "data/version.json")
    isversion, server_url = get_minecraft_url(server_version)
    if not isversion:
        return 2
    match edition:
        case 'vanilla':
            download_file(server_url, minecraft_dir+"/server.jar", user_agent="")
            start_jar = "server.jar"
        case 'spigot':
            if spigot_download(server_version) == False:
                return 3
            start_jar = "server.jar"
        case 'forge':
            if install_forge_server(minecraft_dir, server_version, forge_id) == False:
                return 4
            start_jar = "forge-"+server_version+"-"+forge_id+".jar"
        case _:
            return 1
    
    download_file("https://server.properties/", minecraft_dir+"/server.properties")
    file_identification_rewriting(minecraft_dir+"/server.properties", "server-port=", "server-port="+str(server_port)+"\n")
    file_identification_rewriting(minecraft_dir+"/server.properties", "motd=", "motd="+server_name+"\n")
    f = open(minecraft_dir+"/eula.txt", 'w')
    f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#"+dt_now_utc.strftime('%a')+" "+dt_now_utc.strftime('%b')+" "+dt_now_utc.strftime('%d')+" "+dt_now_utc.strftime('%H:%M:%S')+" "+str(dt_now_utc.tzinfo)+" "+dt_now_utc.strftime('%Y')+"\neula="+str(eula))
    f.close()
    with open("./data/setting.ini", mode='a') as f:
        f.write('['+minecraft_dir.lower()+']\nstart_jar = '+start_jar+'\nserver_name = '+server_name+'\n')


make("test", 25565, "1.12.2", "forge", "14.23.5.2860",True,True)