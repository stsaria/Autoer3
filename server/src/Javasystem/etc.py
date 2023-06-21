import subprocess

def exec_java(dir_name, jar_name, xms, xmx, java_argument=""):
    """javaを実行するための関数"""
    # もし入力内容が0かnotだったら1(1GB)に
    cmd = "java -Xmx"+str(xmx)+"G -Xms"+str(xms)+"G -jar ./"+jar_name+" "+java_argument
    subprocess.call(cmd, shell=True, cwd=dir_name+"/")