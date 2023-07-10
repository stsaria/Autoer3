import subprocess, re

def java_version():
    java_version = str(re.findall('".+"',
                                    str(subprocess.run('java -version', capture_output=True, text=True, shell="True").stderr))).replace('"', '').replace("'", "").replace('[', '').replace(']', '')
    
    java_version_base = str(re.search(r'\d+', java_version).group())
    if java_version[:3] == "1.8":
        java_version_base = "8"
    return java_version, java_version_base

def minecraft_to_support_list(minecraft_version):
    java_version_base = java_version()[1]
    minecraft_version_two_base = str(re.search(r'\d+', minecraft_version[2:]).group())
    support = False
    if 1 <= int(minecraft_version_two_base) <= 6 and int(java_version_base) == 8:
        support = True
    if  7 <= int(minecraft_version_two_base) <= 16 and 8 <= int(java_version_base) <= 11 and not 9 <= int(java_version_base) <= 10:
        support = True
    if int(minecraft_version_two_base) == 17 and int(java_version_base) == 16:
        support = True
    if 18 <= int(minecraft_version_two_base) <= 99 and int(java_version_base) == 17:
        support = True
    return support
