import subprocess, re

def java_version():
    try:
        java_version = str(re.findall('".+"',
                                        str(subprocess.run('java -version', capture_output=True, text=True, shell="True").stderr))).replace('"', '').replace("'", "").replace('[', '').replace(']', '')
        
        java_version_base = str(re.search(r'\d+', java_version).group())
        if java_version[:3] == "1.8":
            java_version_base = "8"
        return True, [java_version, java_version_base]
    except:
        return False, [None, None]
