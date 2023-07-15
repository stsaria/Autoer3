import subprocess

def exec_java(dir_name, jar_name, xms : int, xmx : int, java_argument="nogui"):
    """javaを実行するための関数"""
    subprocess.run(f"java -Xmx{str(xmx)}G -Xms{str(xms)}G -jar {jar_name} {java_argument}", shell=True, cwd=f"{dir_name}/", check=True)