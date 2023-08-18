# Autoer3

## Autoer3とAutoerとは
Autoer3とはAutoer系統のプログラムです
<br/>Autoerはマイクラを半自動作成するプログラムです

## 条件
1.ネットワーク環境がある
<br/>2.Python3.10以上
<br/>3.requestsがインストールされてる
<br/>※実行ファイルの場合はインストール不要

## 導入
1.Releaseからソースコードをダウンロードします
<br/>※実行ファイルでも問題ないです
<br/>2.Pythonのrequestsをダウンロードします
<br/>`$ pip install requests`
<br/>3.Autoerを実行します
<br/>`$ python src/Autoer.py`
<br/>もしくは
<br/>`$ ./Autoer`
<br/>次のように引数を与えずに実行すると引数の与え方の説明が出ます

## 注意
・このプログラムを不正に使わないでください

## 引数の使い方
```Autoer -[s,m,bs,bm,R,r,cp,sl,sysdm,sysdr,se,trans,legacy-trans] [etc_args]```
### 引数欄:
#### 起動モード:
-s,-m : 作成<br/>
(方法 : ```-m [server_name (スペース, タブなし)] [server_port (1~65535)] [server_version (プレリリース版でも可※)] [eula (true or false)] [server_edition (vanilla, spigot, forge, paper)] [build_id (Forge※, PaperMC※ 使用時のみ)]```)<br/>
※プレリリース版はForge, PaperMCとの組み合わせでは使えません<br/>
※ForgeはBuildIDの取得ができません<br/>
※PaperMCはBuildIDを省略すれば自動的に新しいjarファイルがダウンロードされます<br/>

-bs,-bm : Bungeecordの作成<br/>
(方法 : ```-bm [server_name (スペース, タブなし)] [server_port (1~65535)]```)<br/>

-auto 限りなく自動に近いサーバー作成<br/>
(方法 : ```-auto [server_name (スペース, タブなし)] [eula (true or false)]```)<br/>
上記以外はこちらで作成されます<br/>
Version : 最新<br/>
Port : 25565<br/>
Edithon : Vanilla<br/>
管理者の場合は自動起動設定を実行します<br/>

-R : 削除<br/>
(方法 : ```-R [server_id]```)<br/>

-r : 起動<br/>
(方法 : ```-r [server_id] [Xms (int)(最小メモリ)] [Xmx (int)(最大メモリ)]```)<br/>

-sl : サーバーリストの表示<br/>
(方法 : ```-sl```)<br/>

-cp : サーバーのポート変更<br/>
(方法 : ```-cp [server_id] [server_new_port (1~65535)]```)<br/>

-sysdm,-sysds サーバーをSystemd Deamon,スタートアップに登録する(自動起動設定)(※管理者権限が必須です)<br/>
(方法 : ```-sysdm [server_id] [Xms (int)(最小メモリ)] [Xmx (int)(最大メモリ)] -screen (Screenでの起動(Windows以外))```)<br/>

-sysdr サーバーのSystemd Deamon,スタートアップを削除する(自動起動解除)(※管理者権限が必須です)<br/>
(方法 : ```-sysdr [server_id]```)<br/>

-se サーバー管理ファイルの編集モード(Minecraftでserver.propeties、Bungeecordでconfig.yml)<br/>
(方法 : ```-se [server_id] [editer(Windows以外)]```)<br/>

-trans サーバーの情報を移行するモード(Minecraftでworld, world_nether, world_the_end, server.properties, spigot.yml(Spigot, Paperのみ)、Bungeecordでconfig.yml)<br/>
(方法 : ```-trans [before_server_id (移行元のサーバー)] [after_server_id (移行先のサーバー)] -minimum (必要最低限のファイル)```)<br/>

-unsupported-trans Autoerではないサーバーを-transのように移行できるモード<br/>
(方法 : ```-unsupported-trans [before_server_id_or_dir (移行元のサーバー)] [after_server_or_id (移行先のサーバー)] -minimum (必要最低限のファイル)```)<br/>

-html, -reload-html サーバー一覧をHTMLに出力するモード<br/>
(方法 : ```-html [path(任意)]```)<br/>

※server_id は サーバー作成時に発行されたID(-sl(サーバーリスト表示)でIDを確認することができます)