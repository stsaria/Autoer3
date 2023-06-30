import threading, asyncio, time, cgi, os
from ....src import MakeServer
form = cgi.FieldStorage()
server_name = form.getfirst('server_name')
server_port = form.getfirst('server_port')
server_version = form.getfirst('server_version')
server_mode = form.getfirst('server_mode')
forge_id = form.getfirst('forge_id')
eula = form.getfirst('eula')

for i in [server_name, server_port, server_version, server_mode]:
    if i == "":
        print("Content-Type: text/html",flush=True)
        print(flush=True)
        print( '<head><meta http-equiv="refresh" URL="cgi-bin/Autoer.py"></head><script type="text/javascript">document.location.href = "Autoer.py?m=input_failed";</script>'.encode("cp932", 'ignore').decode('cp932'),flush=True )


async def make():
    MakeServer.make(server_name, int(server_port), server_version, server_mode, False, eula, forge_id)
asyncio.run(make())

# ブラウザに戻すHTMLのデータ
print("Content-Type: text/html",flush=True)
print(flush=True)
htmlText = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="shift-jis" />
        <script>
            window.onbeforeunload = function(event){
                event = event || window.event; 
                event.returnValue = 'ページから移動しますか？';
            }
            window.addEventListener('popstate', function(e) {window.onbeforeunload = "a";});
        </script>
    </head>
    <body bgcolor="lightyellow">
        <h1>現在サーバー作成中です</h1>
        <h2>しばらくお待ち下さい</h2>
        サーバーの作成はネットワークの調子などによっても変わります。
    </body>
</html>
''' # 入力値の積を%sの箇所に埋める
print( htmlText.encode("cp932", 'ignore').decode('cp932'),flush=True )