import maze_maker as mk
import tkinter as tk
import pprint

#5. 関数key_downを定義し、"<KeyPress>"イベントと紐づける
#グローバル変数keyに押されたキーのシン折るkeysymを代入する
def key_down(event):
    global key
    key = event.keysym
    main_proc()
    
#6. 関数key_upを定義し、"<KeyRelease>"イベントと紐づける
#グローバル変数keyに空文字列""を代入する
def key_up(event):
    global key
    key = ""
  

#7. 常時起動するリアルタイム処理関数main_proc()を定義する
def main_proc():
    global cx, cy, key, canvas, my_pos
    try:
        if key == "Up":
            if (maze_list[my_pos[1] - 1][my_pos[0]]) == 0:
                pass
            else:
                cy -= 100
                my_pos[1] -= 1
                
        elif key == "Down":
            if (maze_list[my_pos[1] + 1][my_pos[0]]) == 0:
                pass
            else:
                cy += 100
                my_pos[1] += 1
                
        elif key == "Left":
            if (maze_list[my_pos[1]][my_pos[0] - 1]) == 0:
                pass
            else:
                cx -= 100
                my_pos[0] -= 1
                
        elif key == "Right":
            if (maze_list[my_pos[1]][my_pos[0] + 1]) == 0:
                pass
            else:    
                cx += 100
                my_pos[0] += 1
                
    except IndexError as e:
        pass
            
    canvas.coords("chr", cx, cy)
    
            
if __name__ == "__main__":
    #1.ゲーム用のウィンドウを生成する.
    root = tk.Tk()
    root.title("迷路")
    
    key = ""   #4. グローバル変数keyを空文字列で初期化する
    
    #2. 幅 : 1500, 高さ : 900, 背景色 : blackのCanvasを生成する.
    canvas = tk.Canvas(width = 1500, height = 900, bg = "black")
    canvas.pack()
    
    maze_list = mk.make_maze(15, 9)
    mk.show_maze(canvas, maze_list)   #10. maze_makerモジュールのshow_maze関数を呼び出し、迷路を描画する
    
    #3.figフォルダ内の好きなこうかとんのインスタンスを生成し、Canvas内における横 : 300, 縦400の座標に表示させる
    my_pos = [0, 0]   #自身のいるマスを保持する. 左上を[0, 0], 右上を[14, 0], 左下を[9, 0], 右下を[9, 15]と表す
    cx, cy = 50, 50
    image_file = "fig/1.png"
    chr = tk.PhotoImage(file = image_file)
    canvas.create_image(cx, cy, image = chr, tag = "chr")
        
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    
    canvas.mainloop()