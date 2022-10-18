import maze_maker as mk
import tkinter as tk

#1.ゲーム用のウィンドウを生成する.
#2. 幅 : 1500, 高さ : 900, 背景色 : blackのCanvasを生成する.
canvas = tk.Tk()
canvas.title("迷路")
canvas.geometry("1500x900")

#3.figフォルダ内の好きなこうかとんのインスタンスを生成し、Canvas内における横 : 300, 縦400の座標に表示させる
#x座標をcx, y座標をcyとする
cx, cy = 300, 400
image_file = "fig/1.png"
chr = tk.PhotoImage(file = image_file)
canvas.create_image(cx, cy, image = chr, tag = "chr")

#4. グローバル変数keyを空文字列で初期化する
key = ""

#5. 関数key_downを定義し、"<KeyPress>"イベントと紐づける
#グローバル変数keyに押されたキーのシン折るkeysymを代入する
def key_down(event):
    global key
    key = event.keysym
    
#関数key_upを定義し、"<KeyRelease>"イベントと紐づける
#グローバル変数keyに空文字列""を代入する
def key_up(event):
    global key
    key = ""
  
"""  
#常時起動するリアルタイム処理関数main_proc()を定義する
#グローバル変数cx, cyの値を適切に増減することで、キャラを動かす
#グローバル変数keyの値によって動きを分ける
#UP : 上に20
#Down : 下に20
#Left : 左に20
#Right : 右に20
#canvasクラスのインスタンスメソッドcoordsで座標を更新する
#mainproc()を呼び出し、常時起動するようにする
"""
def main_proc():
    global cx, cy, key
    if key == "Up":
        cy += 20
    elif key == "Down":
        cy -= 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20
        
    canvas.coords(chr, cx, cy)    
            
    
main_proc()    
canvas.mainloop()