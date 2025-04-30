# アークナイツ公開求人検索機

## 🔧 実行方法
`アークナイツ公開求人検索機.exe` をダブルクリックして実行できます（Windows用）

## 📦 exeファイルの再作成
1. `ope.txt` と `ope_img/` フォルダを`アークナイツ公開求人検索機.py`と同じディレクトリに置いてください
2. 以下のコマンドを入力して実行

pyinstaller --onefile --noconsole --add-data "ope_img;ope_img" --add-data "ope.txt;." アークナイツ公開求人検索機.py
