import pygame as pg
import sys
import random

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
    global g, bomb_vx, bomb_vy, bomb_x, bomb_y, bomb_rect_obj
    bomb_x += bomb_vx
    bomb_y += bomb_vy
    
    bomb_rect_obj.center = bomb_x, bomb_y   # bomb_objの位置を更新する
 
   
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
                
        if event.type == pg.MOUSEMOTION:   # マウスカーソルを動かしたとき、各座標を取得する
            mouse_x, mouse_y = pg.mouse.get_pos()
            
        if event.type == pg.MOUSEBUTTONDOWN:   # マウスボタンを離したとき、ボタンを離したかを判定する変数に保存する
            left_button, right_button, wheel_button = pg.mouse.get_pressed()
            
        if event.type == pg.MOUSEBUTTONUP:
            left_button, right_button, wheel_button = pg.mouse.get_pressed()
        

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
    chr_image_rect = chr_image.get_rect()
    chr_x, chr_y = 900, 400
    chr_image_rect.center = 900, 400
        
        
def setup_bomb_image():
    """ 
    5. 爆弾を作りランダムな場所に配置する
    """
    global bomb_vx, bomb_vy, bomb_x, bomb_y, bomb_rect_obj
    bomb_vx, bomb_vy = 1, 1
    bomb_x, bomb_y = random.randint(10, 1590), random.randint(10, 890)
    bomb_rect_obj = pg.draw.circle(g, (255, 0, 0), (bomb_x, bomb_y), 10.0, width = 0)


def collision_to_wall_detect():
    """ 
    7. こうかとんと爆弾が画面の外に出ないようにする
    """
    global chr_x, chr_y, bomb_vx, bomb_vy, bomb_x, bomb_y
    if chr_x > 1500:
        chr_x = 1500
        
    if chr_x < 0:
        chr_x = 0
        
    if chr_y > 760:
        chr_y = 760
        
    if chr_y < 0:
        chr_y = 0
    
    if bomb_x > 1600 - 10 or bomb_x < 0 + 10:
        bomb_vx *= -1
        
    if bomb_y > 900 - 10 or bomb_y < 0 + 10:
        bomb_vy *= -1
        
    chr_image_rect.center = chr_x, chr_y   #Rectオブジェクトの位置更新
    bomb_rect_obj.center = bomb_x, bomb_y   # bomb_objの位置を更新する
    
    
def collision_to_bomb_detect():
    """ 
    8. こうかとんと爆弾が衝突したことを判定する
    """
    global chr_x, chr_y, bomb_vx, bomb_vy, bomb_x, bomb_y, chr_image_rect, bomb_rect_obj, collision_detect
    collision_detect = chr_image_rect.colliderect(bomb_rect_obj)   # こうかとんと爆弾が衝突したかを判定する
    if collision_detect == True:
        sys.exit()


if __name__ == "__main__":
    pg.init()
    g = pg.display.set_mode((1600, 900))
    setup_chr_image()      # 3. こうかとんの生成
    setup_bomb_image()     # 5. 半径10, 色赤の爆弾を作り、ランダムな場所に配置する
        
    while True:
        clock_obj = pg.time.Clock()
        setup_surface()        # 1. ウィンドウの生成
        setup_back_image()     # 2. 背景の生成
        get_event_queue()      # eventqueueの取得
        
        chr_move_update()      # 4. こうかとんの位置を更新する
        bomb_move_update()     # 6. 爆弾の位置を更新する
        
        collision_to_wall_detect()   # 7. 壁に当たったときのオブジェクトの位置を更新する
        collision_to_bomb_detect()   # 8. こうかとんと爆弾がぶつかったかどうかを判定する
        
        g.blit(chr_image, (chr_x, chr_y))   # こうかとんを表示
        pg.draw.circle(g, (255, 0, 0), (bomb_x, bomb_y), 10.0, width = 0)   # 爆弾を表示
        
        pg.display.update()    # 2. display.update()
        clock_obj.tick(1000)   # 2. 1000[fps]