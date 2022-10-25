import pygame as pg
import sys
import random
from itertools import combinations

def chr_move_update():
    """ 
    4. 矢印キーによりこうかとんが移動できるようにする
    """
    global key_list, chr_image, chr_x, chr_y, chr_image_rect
    if key_list[pg.K_UP] == True:
        chr_y -= 5
    
    if key_list[pg.K_DOWN] == True:
        chr_y += 5
        
    if key_list[pg.K_LEFT] == True:
        chr_x -= 5
        
    if key_list[pg.K_RIGHT] == True:
        chr_x += 5
        
    chr_image_rect.center = chr_x, chr_y   #Rectオブジェクトの位置更新
        
        
def bomb_move_update():
    """ 
    6. 爆弾を移動させる
    """
    global bombs_list
    for i in range(len(bombs_list)):
        bombs_list[i][0] += bombs_list[i][2]
        bombs_list[i][1] += bombs_list[i][3]
        
        bombs_list[i][4].center = bombs_list[i][0], bombs_list[i][1]
 
   
def get_event_queue():
    """ 
    eventqueueを取得し、取得状態を更新する
    """
    global key_list, mouse_x, mouse_y, left_button, right_button, wheel_button
    for event in pg.event.get():
        key_list = pg.key.get_pressed()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()   # 2. ×ボタンが押された時の処理
                
        if event.type == pg.KEYDOWN:       # キーを押したとき            
            if event.key == pg.K_ESCAPE:   # Escキーが押されたとき
                pg.quit()
                sys.exit()
                    
        if event.type == pg.KEYUP:   # キーが離された時
            key_list = pg.key.get_pressed()


def setup_surface():
    """ 
    1. ウィンドウを生成する
    """
    global g
    g = pg.display.set_mode((1600, 900))   # 1. ウィンドウ生成
    g.fill((0, 0, 0))
    g.set_colorkey((0, 0, 0))
    pg.display.set_caption("逃げろ！こうかとん")


def setup_back_image():
    """ 
    2. 背景を生成する
    """
    global g, back_image
    back_image = pg.image.load("pg_bg.jpg")   # 2. 背景作成Image_obj
    g.blit(back_image, (0, 0))                # 2. 背景画像をblit
        
        
def setup_chr_image():
    """ 
    3. こうかとんを生成する
    """
    global chr_image, chr_x, chr_y, chr_image_rect
    chr_image = pg.image.load("fig/0.png")   # 3. こうかとん作成
    chr_image = pg.transform.rotozoom(chr_image, 0, 2.0)   # 3. 2倍に拡大
    chr_image_rect = chr_image.get_rect()   # chrのRectオブジェクトを生成
    chr_x, chr_y = 900, 400   # こうかとんの座標を指定
    chr_image_rect.center = 900, 400   # こうかとんのRectオブジェクトの位置を更新
        
        
def setup_bomb_image():
    """ 
    5. 爆弾を作りランダムな場所に配置する
    """
    global bomb_vx, bomb_vy, bomb_x, bomb_y, bomb_rect_obj
    l = [-1, 1]   # 初期速度
    bomb_vx, bomb_vy = random.choice(l), random.choice(l)   # 初期のx方向速度とy方向速度をランダムに指定
    bomb_x, bomb_y = random.randint(10, 1590), random.randint(10, 890)   # 初期の爆弾の位置をランダムに指定
    bomb_rect_obj = pg.draw.circle(g, (255, 0, 0), (bomb_x, bomb_y), 10.0, width = 0)   # 爆弾のrectオブジェクトを生成
    
    return [bomb_x, bomb_y, bomb_vx, bomb_vy, bomb_rect_obj]   # のちの爆弾増加のために、座標や速度、Rectオブジェクトを返す


def collision_to_wall_detect():
    """ 
    7. こうかとんと爆弾が画面の外に出ないようにする
    """
    global chr_x, chr_y, bombs_list
    if chr_x > 1550:
        chr_x = 1550
        
    if chr_x < 50:
        chr_x = 50
        
    if chr_y > 830:
        chr_y = 830
        
    if chr_y < 70:
        chr_y = 70
    
    for i in range(len(bombs_list)):
        if bombs_list[i][0] > 1600 - 10 or bombs_list[i][0] < 0 + 10:
            bombs_list[i][2] *= -1
            
        if bombs_list[i][1] > 900 - 10 or bombs_list[i][1] < 0 + 10:
            bombs_list[i][3] *= -1
        
    chr_image_rect.center = chr_x, chr_y   #Rectオブジェクトの位置更新
    
    
def collision_to_bomb_detect():
    """ 
    8. こうかとんと爆弾が衝突したことを判定する
    """
    for bx, by, bvx, bvy, b_obj in bombs_list:
        collision_detect = chr_image_rect.colliderect(b_obj)   # こうかとんと爆弾が衝突したかを判定する
        if collision_detect == True:
            sys.exit()   # 衝突したらプログラムを抜ける


def obj_show():
    """ 
    画面上を動くオブジェクトを表示する
    """
    g.blit(chr_image, chr_image_rect)   #(chr_x, chr_y))   # こうかとんを表示
    for bx, by, bvx, bvy, b_obj in bombs_list:   # 爆弾リストに入っている爆弾を表示
        pg.draw.circle(g, (255, 0, 0), (bx, by), 10.0, width = 0)   # 爆弾を表示


def time_update():
    """ 
    ゲーム時間を更新し、時間を表示、時間に合わせて爆弾を増加させる
    """
    global g, time, bombs_list
    time += 1   # ゲームの経過時間を更新する
    if time % 500 == 0:   # 5[s]おきに
        for i in bombs_list:   #核爆弾の速度を増加させる
            if i[2] > 0:
                i[2] += 0.5
            else:
                i[2] -= 0.5
            if i[3] > 0:
                i[3] += 0.5
            else:
                i[3] -= 0.5
        bombs_list.append(setup_bomb_image())   # 爆弾を増やす
        
    font = pg.font.Font(None, 80)
    text = font.render(f"time : {time // 100}[s]", True, (255, 0, 0))
    g.blit(text, (10, 0))   #ゲーム内時間を表示する
    

def bomb_collision_to_bomb_detect():
    """
    爆弾同士の衝突判定を行い、速度を変化させる
    """
    global bombs_list
    c = combinations(bombs_list, 2)   # itertoolsのconbinations関数を利用することで、重複なしの組み合わせを取得する. [[x, y, vx, vy, obj], ...]
    for i in c:
        collision_detect = i[0][4].colliderect(i[1][4])   # 組み合わせから、衝突したかを判定する
        if collision_detect == True:
            for j in bombs_list:   #衝突したら
                if j[4] == i[0][4]:   #双方の爆弾のx方向速度の符号を反転させる
                    j[2] *= -1
                elif j[4] == i[1][4]:
                    j[2] *= -1


if __name__ == "__main__":
    pg.init()
    g = pg.display.set_mode((1600, 900))
    time = 0
    bombs_list = []   # 増加した爆弾を格納しておくリスト(2次元)
    setup_chr_image()      # 3. こうかとんの生成
    bombs_list.append(setup_bomb_image())     # 5. 半径10, 色赤の爆弾を作り、ランダムな場所に配置する. 作成した爆弾を爆弾リストに格納する
        
    while True:
        clock_obj = pg.time.Clock()

        setup_surface()        # 1. ウィンドウの生成
        setup_back_image()     # 2. 背景の生成
        get_event_queue()      # eventqueueの取得
        time_update()          # 時間の更新
        
        chr_move_update()      # 4. こうかとんの位置を更新する
        bomb_move_update()     # 6. 爆弾の位置を更新する
        
        collision_to_wall_detect()   # 7. 壁に当たったときのオブジェクトの位置を更新する
        collision_to_bomb_detect()   # 8. こうかとんと爆弾が衝突したかを判定する
        bomb_collision_to_bomb_detect()   # 爆弾と爆弾が衝突したかを判定する
        
        obj_show()
        
        pg.display.update()    # 2. display.update()
        clock_obj.tick(1000)   # 2. 1000[fps]