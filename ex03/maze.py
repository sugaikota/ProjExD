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

canvas.mainloop()