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
        <title>Autoer3 管理画面</title>
    </head>
    <body bgcolor="lightyellow">
        <h1>Autoer3 - 管理画面</h1>
        <h2>サーバー一覧</h2>
        <h4>%s</h4>
        <hr/>
        <h2>サーバー作成</h2>
        <form action="make.py" method="post">
            <h4>注意 Forgeではforgeのビルド番号を求められます</br>事前にご確認ください</h4>
            <input type="text" name="server_name" placeholder="サーバー名："></p>
            <input type="text" name="server_port" placeholder="ポート番号："></p>
            <input type="text" name="server_port" placeholder="バージョン："></p>
            <p>サーバーの種類（バニラ、プラグイン(Spigot)、Mod鯖(Forge)）：<br>
            <select id="server_mode" name="server_mode" onchange="window.event();">
                <option value="vanilla">バニラ</option>
                <option value="spigot">Spigot</option>
                <option value="forge">Forge</option>
            </select></p>
            <input type="text" id="forge_id" name="forge_id" placeholder="Forgeのビルド番号">
            <input type="checkbox" name="eula" value="Eulaに同意する" id="eula"></p>
            <script type="text/javascript">
                document.getElementById('forge_id').style.display = 'none'
                console.log(document.getElementById("servermode").value)
                function event(){
                    console.log(document.getElementById("server_mode").value)
                    if(document.getElementById("servermode").value == "forge"){
                        document.getElementById('forge_id').style.display = ""
                    } else {document.getElementById('forge_id').style.display = 'none'}
                }
                window.onload = event;
            </script>
            <p><input type="submit" value="これで作成"></p>
        </form>
        <button>もう一つ作成</button>
'''%(show_text) # 入力値の積を%sの箇所に埋める
print( htmlText.encode("cp932", 'ignore').decode('cp932') )
if form.getfirst('m'):
    if form.getfirst('m') == "input_failed":
        print('<font color="#ff0000"><h2>サーバーの作成に失敗しました 詳細:入力方式が間違っています。</h2>')
    if form.getfirst('m') == "exception_failed":
        print('<font color="#ff0000"><h2>サーバーの作成に失敗しました 詳細:サーバー作成時に例外が発生しました。</h2>')
print("</body>\
</html>")