import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk #type: ignore
from pathlib import Path

tag_list=["ロボット","初期","エリート","上級エリート","近距離","遠距離","先鋒タイプ","前衛タイプ","重装タイプ","狙撃タイプ","術師タイプ","医療タイプ","補助タイプ","特殊タイプ",
          "火力","生存","防御","治療","範囲攻撃","減速","COST回復","支援","弱化","強制移動","高速再配置","爆発力","牽制","召喚"]

# 新しいウィンドウを作成
root = tk.Tk()

# ウィンドウのタイトルを設定
root.title("公開求人検索機")

# 16:9の解像度を設定（ここではフルHD）
width = 960
height = 540
root.geometry(f"{width}x{height}")

# ウィンドウの背景色を白に設定
root.configure(bg='white')

# チェックボタンの変数を作成
checkbutton_var = tk.IntVar()

# チェックボタンの幅と高さを設定
button_width = 8
button_height = 2

checkbutton_vars=[]
names_and_tags = []

button_space_x=90
button_space_y=50

x=10
y=10

tag_count=0
max_selected_tags = 3  # 最大で選択できるタグの数

# 選択されたタグ数の制限
def checkbutton_command(var):
    selected_count = sum(v.get() for v in checkbutton_vars)
    if selected_count > max_selected_tags:
        var.set(0)  # 上限を超えた場合はチェックを外す

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

# ファイルから読み取ってList化
def load_file_list(filename):
    base_path = resource_path('ope_img')  # 画像フォルダ
    file_path = resource_path(filename)   # ope.txt のパス

    with open(file_path, 'r', encoding='utf-8') as file:
        names = file.read().splitlines()

    for line in names:
        parts = line.split()  # スペースで分割
        name = parts[0]       # 最初の部分は名前
        tags = parts[1:]      # タグ部分
        img_path = base_path / (name + '.jpg')  # 画像ファイルのパス
        names_and_tags.append([name, tags, img_path])

    return names_and_tags

# ope.txtからリストを読み込む
ope_list = load_file_list('ope.txt')

# 選択されたタグの名前を取得する関数
def get_selected_tag_names():
    selected_tags = []
    for i, var in enumerate(checkbutton_vars):
        if var.get():
            selected_tags.append(tag_list[i])
    return selected_tags

# 絞り込み結果を表示する新しいウィンドウを作成
def show_results_window(filtered_results):
    results_window = tk.Toplevel(root)
    results_window.title("検索結果")
    results_window.geometry(f"{width}x{height}")

    # スクロール機能を追加
    canvas = tk.Canvas(results_window)
    scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    if not filtered_results:
        # 検索結果がない場合のメッセージ表示
        no_results_label = tk.Label(results_window, text="対象者がいません", font=("Helvetica", 25))
        no_results_label.pack(expand=True, pady=250)
    else:
        # 検索結果を表示
        max_columns = 10
        column_count = 0
        row_count = 0
        for i, (name, img_path) in enumerate(filtered_results):
            # 名前を表示
            name_label = tk.Label(scrollable_frame, text=name)
            name_label.grid(row=row_count * 2, column=column_count, padx=10, pady=10)

            # 画像を表示
            try:
                img = Image.open(img_path)
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                img_label = tk.Label(scrollable_frame, image=img)
                img_label.image = img  # 画像を保持しておくために必要
                img_label.grid(row=row_count * 2 + 1, column=column_count, padx=10)
            except Exception as e:
                print(f"画像の読み込みエラー: {e}")

            column_count += 1
            if column_count >= max_columns:
                column_count = 0
                row_count += 1

    # 終了ボタンを追加
    quit_button = tk.Button(results_window, text="終了", command=results_window.destroy, bg="red", fg="white", font=("Helvetica", 14, "bold"))
    quit_button.place(x=width-100, y=height-50)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# 選択されたタグの名前を取得する関数
def get_selected_tag_names():
    selected_tags = []
    for i, var in enumerate(checkbutton_vars):
        if var.get():
            selected_tags.append(tag_list[i])
    return selected_tags

# 検索ボタンを押した時の処理
def show_checkbutton_states():
    selected_tags = get_selected_tag_names()
    if len(selected_tags) == 0:
        # 検索結果がない場合のメッセージ表示
        no_tags_label = tk.Label(root, text="tagが選択されていません", font=("Helvetica", 25), bg=root.cget('bg'))
        no_tags_label.pack(padx=10, pady=250)

        # 2秒後にラベルを消去する
        root.after(1500, no_tags_label.destroy)
        return
    
    filtered_results = []

    # タグをすべて含むエントリを絞り込み
    for entry in names_and_tags:
        name, tags, img_path = entry
        if all(tag in tags for tag in selected_tags):
            # 上級エリートが選択されていない場合は上級エリートを持つものを除外
            if "上級エリート" in tags and "上級エリート" not in selected_tags:
                continue
            filtered_results.append((name, img_path))
    show_results_window(filtered_results)

# チェックマークをリセットする関数
def reset_checkbuttons():
    for var in checkbutton_vars:
        tag_count=0
        var.set(0)  # IntVarを0に設定してチェックを外す

for i in range(len(tag_list)):
    var = tk.IntVar()  # チェックボックスの状態を管理するためのIntVarを作成
    checkbutton_vars.append(var)
    checkbutton = tk.Checkbutton(root, text=tag_list[i], variable=var, width=button_width, height=button_height, command=lambda v=var: checkbutton_command(v))
    checkbutton.place(x=x, y=y)
    
    # 次のチェックボタンのx座標を更新
    x += button_space_x
    
    # 画面端に達したら改行
    if x + button_space_x > width:
        x = 10  # x座標をリセット
        y += button_space_y  # y座標を次の行に移動

# 各要素が含まれているかどうかを判定して配列化する
result = []
for name, tags ,img_path in names_and_tags:
    row = []
    for tag in tag_list:
        if tag in tags:
            row.append(1)
        else:
            row.append(0)
    result.append([name] + row)

# 検索ボタンを追加
show_button = tk.Button(root, text="検索開始", command=show_checkbutton_states, bg='#28A745', fg='white', font=("Helvetica", 12, "bold"))
show_button.place(x=10, y=500)

# リセットボタンを追加
reset_button = tk.Button(root, text="リセット", command=reset_checkbuttons, bg='#FFC107', fg='white', font=("Helvetica", 12, "bold"))
reset_button.place(x=130, y=500)

# 終了ボタンを追加
quit_button = tk.Button(root, text="終了", command=root.destroy, bg='#DC3545', fg='white', font=("Helvetica", 12, "bold"))
quit_button.place(x=250, y=500)

# ウィンドウを表示
root.mainloop()