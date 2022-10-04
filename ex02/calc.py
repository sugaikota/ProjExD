import tkinter as tk
import tkinter.messagebox as tkm
""" 
練習問題calc.py(電卓作成)
1. 300x500のウィンドウを作成せよ
2. 0 - 9の数字が書かれたボタンを作成し、電卓のように配置せよ
・幅 : 4, 高さ : 2
・フォント : ("Times New Roman", 30)
・gridでrowとcolumnを設定
3. 10個のボタンに、クリックした際の反応を定義せよ
・showinfoで"nのボタンがクリックされました"と表示させる
4. テキスト入力欄を10個のボタンの上部に追加せよ
・right : 10, width : 10, font : (Times New Roman, 40)
・配置したときにgridにcolumnspanを設定する
5. クリックした際の反応を以下のように変更せよ
・4. のテキスト入力欄にクリックしたボタンの数字を挿入する
・挿入位置はtk.ENDを指定する
・tk.ENDで半句、0と指定した場合も試す
6. あいているばしょに"+"ボタンを追加し、クリックされた時の反応を関数として定義し、その関数をボタンにbindせよ
7/ 空いている場所に"="ボタンを追加し、クリックされた時の反応を関数を定義し、その関数をボタンにbindせよ
・4. のテキスト入力欄の数式を取得し、四季を評価、表示内容の削除、計算結果を挿入する
・数式の取得にはget()メソッドを用いる
・四季の評価にはeval()巻子を用いる
・表示内容の削除にはdelete()メソッドを用いる
・計算結果の挿入にはinsert()メソッドを用いる
"""

def button_click(event):
    """
    ボタンを押したときの反応する
    """
    button = event.widget
    text = button["text"]
    tkm.showinfo("情報", f"{text}のボタンがクリックされました")

def get_button_info(event):
    button = event.widget
    text = button["text"]
    return text
    
root = tk.Tk()   
root.title("電卓")
size = "300x600"
f = ("Times New Roman", 30)
root.geometry(size)
  

loc_list = [(3, 0), (2, 2), (2, 1), (2, 0), (1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0)]   #各ボタンの位置を指定する
for i, loc in zip(range(0, 10), loc_list):
    button = tk.Button(root, text = str(i), font = f, width = 4, height = 2)   #各ボタン生成する
    button.grid(row = loc[0] + 1, column = loc[1])   #配置
    button.bind("<1>", button_click)   #button_clickをbindする
    
entry = tk.Entry(width = 10, font = f)
entry.insert(tk.END, "")
entry.grid(row = 0, column = 0, columnspan = 3)   #4 

root.mainloop()