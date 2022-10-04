import tkinter as tk
import tkinter.messagebox as tkm
import math
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
    ボタンが押された時の処理
    """
    button = event.widget
    text = button["text"]
    if text == "+" or text == "-" or text == "*" or text == "/":
        try: 
            if entry.get()[-1] == "+" or entry.get()[-1] == "-" or entry.get()[-1] == "*" or entry.get()[-1] == "/":
                root.after(1, eq_button)
            else:
                entry.insert(tk.END, text)
        except IndexError as e:
            pass
    else:
        entry.insert(tk.END, text)
        
    
def eq_button():
    """
    いい感じに表示(ボタンが押されっぱなしにならないようにする)
    """
    tkm.showwarning("警告", "演算子の後に演算子は設置できません")
        
    
def eq_button_click(event):
    """
    イコールボタンが押された時の処理
    """
    s = entry.get()   #選択された数式. (type = str)
    ans = round((eval(s), 3))
    
    entry.delete(0, tk.END)
    entry.insert(tk.END, ans)   #練習7


def reset_button_click(event):
    """
    リセットボタンが押された時の処理を行う
    """
    entry.delete(0, tk.END)
    root.after(1, reset_button)
    
    
def reset_button():
    """
    いい感じに表示(ボタンが押されっぱなしにならないようにする)
    """
    tkm.showinfo("リセット", "数式がリセットされました")
    
    
def sin_button_click(event):
    """
    sin()ボタンが押された時の処理
    """
    s = entry.get()
    try:
        text = round(math.sin(float(s[-1])), 2)
        
    except IndexError as e:
        pass 
    
    except ValueError as e:
        root.after(1, warning_show)
        
    entry.delete(len(s) - 1, tk.END)
    entry.insert(tk.END, text)
    

def cos_button_click(event):
    """ 
    cos()ボタンが押された時の処理
    """
    s = entry.get()
    try:
        text = round(math.cos(float(s[-1])), 2)
        
    except IndexError as e:
        pass 
    
    except ValueError as e:
        root.after(1, warning_show)
        
    entry.delete(len(s) - 1, tk.END)
    entry.insert(tk.END, text)
    
    
def tan_button_click(event):
    """ 
    tan()ボタンが押された時の処理
    """
    s = entry.get()
    try:
        text = round(math.tan(float(s[-1])), 2)
        
    except IndexError as e:
        pass 
    
    except ValueError as e:
        root.after(1, warning_show)
        
    entry.delete(len(s) - 1, tk.END)
    entry.insert(tk.END, text)
    

def exp_button_click(event):
    """ 
    exp()ボタンが押された時の処理
    """
    s = entry.get()
    try:
        text = round(math.exp(float(s[-1])), 2)
        
    except IndexError as e:
        pass 
    
    except ValueError as e:
        root.after(1, warning_show)
        
    entry.delete(len(s) - 1, tk.END)
    entry.insert(tk.END, text)
    
    
def warning_show():
    tkm.showwarning("警告", "数字以外は関数内に入れられません")

root = tk.Tk()   
root.title("電卓")
size = "400x700"
f = ("Times New Roman", 30)
root.geometry(size)   #練習1

#entryの作成
entry = tk.Entry(width = 10, font = f)
entry.grid(row = 0, column = 0, columnspan = 3)   #練習4

#数字以外のボタンの作成. zip内で、そのボタンで表示するテキスト、そのボタンの位置、bindする関数を置いている
for t, loc, func in zip(["+", "-", "*", "/", "reset", "=", "sin()", "cos()", "tan()", "exp()"], [(2, 3), (3, 3), (4, 3), (5, 3), (5, 1), (5, 2), (1, 0), (1, 1), (1, 2), (1, 3)], [button_click, button_click, button_click, button_click, reset_button_click, eq_button_click, sin_button_click, cos_button_click, tan_button_click, exp_button_click]):
    button = tk.Button(root, text = t, font = f, width = 4, height = 2, justify = "right")
    button.grid(row = loc[0], column = loc[1])
    button.bind("<1>", func) 

#数字ボタンの作成
loc_list = [(3, 0), (2, 2), (2, 1), (2, 0), (1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0)]   #各ボタンの位置を指定する
for i, loc in zip(range(0, 10), loc_list):
    button = tk.Button(root, text = str(i), font = f, width = 4, height = 2, justify = "right")   #各ボタン生成する
    button.grid(row = loc[0] + 2, column = loc[1])   #練習2
    button.bind("<1>", button_click)   #練習3
    
root.mainloop()