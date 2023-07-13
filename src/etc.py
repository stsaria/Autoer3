import platform, ctypes, os

def is_admin():
    user_use_platfrom = platform.system()
    if user_use_platfrom == "Windows":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    else:
        is_admin = os.geteuid() == 0 and os.getuid() == 0
    
    if is_admin:
        return True
    else:
        return False