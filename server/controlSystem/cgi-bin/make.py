from .. import Autoerfun

import socket

'''
   make = M , m
   start = s
   systemd = S
   shfile = sf
   serveroff = SF
   delete = D , d
'''
HOST = 'localhost'
PORT = 58797

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
client_socket, addr = server_socket.accept()

while True:
    data = client_socket.recv(1024)
    if not data:
        print("No Info")
        break
    result = data.decode().split(' ')
    dostr = result[0]

    if dostr == "SF":
        print("User Stop")
        break



    print('', data.decode())

client_socket.close()
server_socket.close()

import cgi
form = cgi.FieldStorage()
server_name = form.getfirst('servername')
server_version = form.getfirst('version')

# ブラウザに戻すHTMLのデータ
print("Content-Type: text/html")
print()
htmlText = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="shift-jis" />
        <script type="text/javascript">
            window.onbeforeunload = function(e) {
                e.returnValue = "ページを離れようとしています。よろしいですか？";
            }
        </script>
    </head>
    <body bgcolor="lightyellow">
        <h1>現在サーバー作成中です</h1>
        <h2>しばらくお待ち下さい</h2>
        サーバーの作成はネットワークの調子などによっても変わります。
    </body>
</html>
''' # 入力値の積を%sの箇所に埋める
print( htmlText.encode("cp932", 'ignore').decode('cp932') )


