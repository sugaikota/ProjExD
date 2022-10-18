import maze_maker as mk
import tkinter as tk
import tkinter.messagebox as tkm
import random 

#5. 関数key_downを定義し、"<KeyPress>"イベントと紐づける
def key_down(event):
    global key
    key = event.keysym
    main_proc()
    goal_check()   #ゴールしたかを判定する


#6. 関数key_upを定義し、"<KeyRelease>"イベントと紐づける
def key_up(event):
    global key
    key = ""
  

def goal_check():
    """ 
    ゴール([14, 8])に到達したかを判定する
    """
    global image_file
    goal_pos_x, goal_pos_y = 13, 7
    if (my_pos_x, my_pos_y) == (goal_pos_x, goal_pos_y):
        image_f = "fig/9.png"
        goal_chr = tk.PhotoImage(file = image_f)
        canvas.create_image(cx, cy, image = goal_chr, tag = "goal_chr")
        root.after(1000, lambda: root.destroy())   #ゴールをすると一秒後にプログラム終了
        tkm.showinfo("congratulations!", "ゴールしました")


#7. 常時起動するリアルタイム処理関数main_proc()を定義する
def main_proc():
    global cx, cy, key, canvas, my_pos_x, my_pos_y
    if key == "Up":
        if (maze_list[my_pos_y - 1][my_pos_x]) == 1:
            pass
        else:
            my_pos_y -= 1
                
    elif key == "Down":
        if (maze_list[my_pos_y + 1][my_pos_x]) == 1:
            pass
        else:
            my_pos_y += 1
                
    elif key == "Left":
        if (maze_list[my_pos_y][my_pos_x - 1]) == 1:
            pass
        else:
            my_pos_x -= 1
                
    elif key == "Right":
        if (maze_list[my_pos_y][my_pos_x + 1]) == 1:
            pass
        else:    
            my_pos_x += 1
            
    cx, cy = my_pos_x * 100 + 50, my_pos_y * 100 + 50
    if collision_detected() == True:
        my_pos_x, my_pos_y = 1, 1
        cx, cy = my_pos_x * 100 + 50, my_pos_y * 100 + 50
        
    canvas.coords("chr", cx, cy)
    
            
def act_obj():
    """ 
    障害物の行動
    """
    global obj_x, obj_y, obj_pos_x, obj_pos_y
    obj_x += random.randint(-1, 1)
    obj_y += random.randint(-1, 1)
    if obj_x <= 1:
        obj_x = 1
    elif obj_x >= 14:
        obj_x = 14
        
    elif obj_y <= 1:
        obj_y = 1
    elif obj_y >= 8:
        obj_y = 8
        
    obj_pos_x, obj_pos_y = obj_x * 100 + 50, obj_y * 100 + 50
    canvas.coords("obj", obj_pos_x, obj_pos_y)
    canvas.after(1000, act_obj)
            
            
def collision_detected():
    """ 
    自キャラがobjに衝突したか"""
    if obj_pos_x == cx and obj_pos_y == cy:
        tkm.showinfo("collision", "障害物と衝突しました")
        return True
    else:
        return False


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
    my_pos_x, my_pos_y = 1, 1   #自身のいるマスを保持する. 左上を[0, 0], 右上を[14, 0], 左下を[9, 0], 右下を[9, 15]と表す
    cx, cy = 150, 150
    image_file = "fig/1.png"
    chr = tk.PhotoImage(file = image_file)
    canvas.create_image(cx, cy, image = chr, tag = "chr")
    
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    
    #邪魔なobjを作る
    obj_x, obj_y = random.randint(0, 15), random.randint(0, 9)   #マスによるobjの座標
    obj_pos_x, obj_pos_y = obj_x * 100 + 50, obj_y * 100 + 50   #座標によるobjの座標
    obj = tk.PhotoImage(file = "fig/5.png")
    canvas.create_image(obj_pos_x, obj_pos_y, image = obj, tag = "obj")
    canvas.after(1000, act_obj)
    
    canvas.mainloop()