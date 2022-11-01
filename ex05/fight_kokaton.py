import pygame as pg
import sys
import random
from itertools import combinations

class Screen:
    """ 
    スクリーン(背景)を表示するクラス
    """
    def __init__(self, title: str, width: int, height: int, file_path: str):
       self.title = title   # タイトル
       self.width = width   # 幅
       self.height = height   # 高さ
       self.file_path = file_path   # ファイル名(もしくは、ファイルパス)
       
       self.sfc = pg.display.set_mode((self.width, self.height))   # スクリーン尿のSurfaceの生成
       pg.display.set_caption(self.title)   # タイトルを設定する
       self.rct = self.sfc.get_rect()   # スクリーン用のRectを取得
       
       self.bgi_sfc = pg.image.load(self.file_path)   # 背景画像用のSurfaceの生成
       self.bgi_rct = self.bgi_sfc.get_rect()   # 背景画像用のRect取得
       
    def blit(self):
        """ 
        Surfaceクラスのblit()メソッドを呼び出す
        """
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
       

class Bird:
    """ 
    こうかとんにまつわることを制御する
    """
    key_delta = {pg.K_LEFT : (-1, 0), pg.K_RIGHT : (1, 0), 
                    pg.K_UP : (0, -1), pg.K_DOWN : (0, 1)}

    def __init__(self, file_path: str, magnification: int, init_pos_x: int, init_pos_y: int):
        self.file_path = file_path   # ファイル名(もしくは、ファイルパス)
        self.mag = magnification   # 拡大率
        self.pos_x = init_pos_x   # 初期x座標
        self.pos_y = init_pos_y   # 初期y座標
        
        self.sfc = pg.image.load(self.file_path)   # 画像用のSurface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, self.mag)   # 拡大率に合わせて拡大する
        self.rct = self.sfc.get_rect()   # 画像用のRect
        self.rct.center = self.pos_x, self.pos_y
        
    def blit(self, sfc: Screen):
        """ 
        Screenオブジェクトのインスタンス変数であるsfc(Surfaceクラス)のインスタンスのblitメソッドを呼び出す
        """
        sfc.sfc.blit(self.sfc, self.rct)
        
    def update(self, sfc: Screen):
        """ 
        keyの押下状態から、こうかとんを動かし、表示する
        """
        for key, value in Bird.key_delta.items():   # 押下状態に応じてこうかとんを移動する
            if key_list[key] == True:
                self.rct.move_ip(value)
                if check_bound(self.rct, sfc.rct) != (1, 1):   # Screen外に存在したら、
                    self.rct.move_ip(((value[0] * (-1)), (value[1] * (-1))))
        
        self.blit(sfc)
     
        
class Bomb:
    def __init__(self, color: tuple, r: int, vx: int, vy: int, sfc: Screen):
        global bomb_list
        self.color = color
        self.r = r
        self.vx, self.vy = vx, vy   # 速度
        
        self.sfc = pg.Surface((20, 20))   # Bomb用のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, (255, 0, 0), (10, 10), self.r)
        self.rct = self.sfc.get_rect()
        
        self.rct.centerx = random.randint(10, sfc.rct.width - 10)
        self.rct.centery = random.randint(10, sfc.rct.height - 10)
        
    def blit(self, sfc: Screen):
        """ 
        blit()をする
        """
        sfc.sfc.blit(self.sfc, self.rct)
        
    def update(self, sfc: Screen):
        """ 
        Bombの制御を制御する
        """
        self.vx *= check_bound(self.rct, sfc.rct)[0]
        self.vy *= check_bound(self.rct, sfc.rct)[1]
        self.rct.move_ip(self.vx,self.vy)
        
        self.blit(sfc)
        
        
class BirdBullet:
    """ 
    こうかとんが発射する弾を制御するクラス
    """    
    def __init__(self, color: tuple, r: int, vx: int, vy: int, bird: Bird):
        self.color = color
        self.r = r
        self.vx, self.vy = vx, vy   # 速度
        
        self.sfc = pg.Surface((20, 20))   # bulllet用のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, (0, 255, 0), (10, 10), self.r)
        self.rct = self.sfc.get_rect()
        
        
        self.rct.centerx, self.rct.centery = bird.rct.centerx, bird.rct.centery
        
    def blit(self, sfc: Screen):
        """ 
        blit()をする
        """
        sfc.sfc.blit(self.sfc, self.rct)
        
    def update(self, sfc: Screen):
        """ 
        Bombの制御を制御する
        """
        global bird_bullet_list
        self.rct.move_ip(self.vx, self.vy)
        self.blit(sfc)
        
        
class Collision:
    """ 
    objどうしが衝突するかを判定するクラス
    """
    def __init__(self, bird: Bird, bomb: Bomb, bullet: BirdBullet):
        self.bird = bird
        self.bomb = bomb
        self.bullet = bullet
        
    def all_col_check(self):
        self.col_bird_to_bomb()
        self.col_bomb_to_bomb()
        self.col_bomb_to_bullet()
        
    def col_bird_to_bomb(self):
        """ 
        こうかとんと爆弾が衝突したかを判定する
        """
        for bomb in bomb_list:
            if bird.rct.colliderect(bomb.rct):
                pg.quit()
                sys.exit()
                
    def col_bomb_to_bullet(self):
        """ 
        爆弾と弾が衝突したかを判定する
        """
        for bullet in bird_bullet_list:
            for bomb in bomb_list:
                if bullet.rct.colliderect(bomb.rct):
                    bird_bullet_list.remove(bullet)
                    bomb_list.remove(bomb)
        
    def col_bomb_to_bomb(self):
        """ 
        爆弾同士が衝突したかを判定する
        """
        c = combinations(bomb_list, 2)   # itertoolsのconbinations関数を利用することで、重複なしの組み合わせを取得する. [[x, y, vx, vy, obj], ...]
        for bombs in c:
            if bombs[0].rct.colliderect(bombs[1].rct):
                for bomb in bomb_list:
                    if bomb == bombs[0]:
                        bomb.vx *= -1
                    elif bomb == bombs[1]:
                        bomb.vx *= -1
        
        
def setup():
    """
    初期設定を行う
    """
    global screen, bird, time, bird_bullet_list, bomb_list, key_list, cool_time
    screen = Screen("負けるな！こうかとん", 1600, 900, "pg_bg.jpg")   # 背景
    bird = Bird("fig/0.png", 2, 600, 300)   # こうかとん
    bomb = Bomb((255, 0, 0), 10, 1, 1, screen)   # Bomb
    time = 0   # 時間
    bird_bullet_list = []   # 弾の入ったリスト
    bomb_list = [bomb]   # 爆弾の入ったリスト
    key_list = pg.key.get_pressed()   # key_list
    cool_time = 0   # 弾の発射クールタイム
       
        
def check_bound(obj_rct: pg.Rect, scr_rct: Screen):
    """
    obj_rctがscr_rct内に存在するかを判定する
    obj_rct : Brid rect_objもしくは、Bomb rect_obj
    scr_rct : Screen rect_obj
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate
 
   
def get_event_queue():
    """ 
    eventqueueを取得し、取得状態を更新する
    """
    global key_list
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()   # 2. ×ボタンが押された時の処理
                
        if event.type == pg.KEYDOWN:       # キーを押したとき
            key_list = pg.key.get_pressed()
            bird_bullet_appearance(bird)   # スペースキーを押すことで、弾を表示
            
            if event.key == pg.K_ESCAPE:   # Escキーが押されたとき
                pg.quit()
                sys.exit()
                    
        if event.type == pg.KEYUP:   # キーが離された時
            key_list = pg.key.get_pressed()


def bird_bullet_appearance(bird: Bird):
    """ 
    birdのbullet(BirdBullet)を出現させる.
    """
    global bird_bullet_list, cool_time
    BIRD_BULLET_NUM = 5
    
    if key_list[pg.K_SPACE] == True:   # スペースキーを押したら 
        if cool_time == 0:
            bird_bullet_list.append(BirdBullet((0, 255, 0), 20, 1, 0, bird))
            cool_time = 100
        else:
            cool_time -= 1
        
    if len(bird_bullet_list) > BIRD_BULLET_NUM:   # 3つ以上の弾があれば
        bird_bullet_list.pop(-1)   # 6個目は削除し、表示させないようにする


def bird_bullet_show(sfc: Screen):
    """ 
    こうかとんが発射した弾を表示する
    """
    global bird_bullet_list
    try:
        for bullet in bird_bullet_list:
        
            if check_bound(bullet.rct, sfc.rct) != (1, 1):
                bird_bullet_list.remove(bullet)
            bullet.update(sfc) 
        
    except:
        pass


def bomb_appearance(sfc: Screen):
    global bomb_list
    BOMB_NUM = 10
    if time % 1200 * 3 == 0:
        bomb_list.append(Bomb((255, 0, 0), 10, 1, 1, sfc))   # Bombの追加
        
    if len(bomb_list) > BOMB_NUM:   # 10つ以上の弾があれば
        bomb_list.pop(-1)   # 11個目は削除し、表示させないようにする
        

def bomb_show(sfc: Screen):
    global bomb_list
    for bomb in bomb_list:
        bomb.update(sfc)
    

def all_col_check():
    """ 
    objどうしが衝突したかを判定する
    """
    global bird, bomb_list, bird_bullet_list
    col_cls = Collision(bird, bomb_list, bird_bullet_list)
    col_cls.all_col_check()


if __name__ == "__main__":
    pg.init()
    setup()   #初期設定
    
    while True:
        clock_obj = pg.time.Clock()
        time += 1
        get_event_queue()
        
        screen.blit()   # 背景表示
        bird.update(screen)   # こうかとん表示
        
        bomb_appearance(screen)   # 爆弾の出現(3秒ごと)
        bomb_show(screen)   # 爆弾の表示
        
        bird_bullet_appearance(bird)
        bird_bullet_show(screen)   # 弾を表示させる
        
        all_col_check()   # 衝突したかを判定する

        pg.display.update()    # 2. display.update()
        clock_obj.tick(500)   # 2. 1000[fps]