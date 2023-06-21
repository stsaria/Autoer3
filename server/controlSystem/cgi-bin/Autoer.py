import configparser, cgi, os
form = cgi.FieldStorage()

show_text = ""

if os.path.isfile("../data/setting.ini"):
    ini = configparser.ConfigParser()
    ini.read('../data/setting.ini', 'UTF-8')
    print(len(list(ini))-0)
    if len(list(ini))-0 < 1:
        show_text = "サーバーはありません"
    for i in range(len(list(ini))):
        if list(ini)[i] == "DEFAULT":
            continue
        show_text = show_text + str(i) + "番 | サーバー名 : " + ini[list(ini)[i]]["server_name"] + " | jarファイル : " + list(ini)[i] + "/" + ini[list(ini)[i]]["start_jar"] + "<br>"
else:
    show_text = "設定ファイルがありません"

# ブラウザに戻すHTMLのデータ
print("Content-Type: text/html")
print()
htmlText = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="shift-jis" />
    </head>
    <body bgcolor="lightyellow">
        <h1>サーバー一覧</h1>
        <h3>%s</h3>
        <hr/>
        <form action="#" method="post">
            <input type="text" name="server_name" placeholder="サーバー名："></p>
            <input type="text" name="server_port" placeholder="ポート番号："></p>
            <p>サーバーの種類（バニラ、プラグイン(Spigot)、Mod鯖(Forge)）：<br>
            <select id="servermode" onclick="event();">
                <option value="vanilla">バニラ</option>
                <option value="spigot">Spigot</option>
                <option value="forge">Forge</option>
            </select></p>
            <input type="text" id="forge_id" placeholder="Forgeのビルド番号">
        </form>
        <script type="text/javascript">
            document.getElementById('forge_id').style.display = 'none'
            function event(){
                if(document.getElementById("servermode").value == "forge"){
                    document.getElementById('forge_id').style.display = ""
                } else {document.getElementById('forge_id').style.display = 'none'}
            }
            window.onload = event;
        </script>
            <p>お問合せ内容：<br>
            <textarea name="comment" cols="30" rows="5"></textarea></p>
            <p><input type="submit" value="確認する"></p>
        </form>
        サーバーの作成はネットワークの調子などによっても変わります。
    </body>
</html>
'''%(show_text) # 入力値の積を%sの箇所に埋める
print( htmlText.encode("cp932", 'ignore').decode('cp932') )