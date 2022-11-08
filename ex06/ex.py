# 制作者 : 菅井
import pygame as pg
import random
import sys


class Screen:
    """ 
    スクリーンを表示するクラス
    """
    def __init__(self, title: str, width: int, height: int):
        """ 
        イニシャライザ
        title : ウィンドウに設定するタイトル
        width : 画面サイズx座標
        height : 画面サイズy座標
        file_path : 背景画像ファイルパス
        """
        self.sfc = pg.display.set_mode((width, height))   # スクリーン用のSurfaceの生成
        pg.display.set_caption(title)   # タイトルを設定する
        self.rct = self.sfc.get_rect()   # スクリーン用のRectを取得
        

class MyTable:
    """ 
    味方台にまつわることを制御する
    """
    def __init__(self, x: int, y: int, vx: int, vy: int, color: tuple=(255, 255, 255)):
        """ 
        イニシャライザ
        color : 色のタプル(tuple)
        x : 初期x座標
        y : 初期y座標
        vx : x座標方向速度
        vy : y座標方向速度
        """
        self.vx, self.vy = vx, vy   # 速度
        self.color = color   # 台の色
        self.key_delta = {pg.K_UP : (0, -vy), pg.K_DOWN : (0, vy)}   # キーによる速度変化
        
        self.rct = pg.Rect(x, y, 10, 30)   # 台のrectオブジェクト生成
        
    def blit(self, sfc: Screen):
        """ 
        Screenオブジェクトのインスタンス変数であるsfc(Surfaceクラス)のインスタンスのblitメソッドを呼び出す
        """
        pg.draw.rect(sfc.sfc, self.color, self.rct)   # 台を描く
        
    def update(self, sfc: Screen):
        """ 
        keyの押下状態から、台を動かし表示する
        """
        for key, value in self.key_delta.items():   # 押下状態に応じてこうかとんを移動する
            if key_list[key] == True:
                self.rct.move_ip(value)
                if check_bound(self.rct, sfc.rct) != (1, 1):   # Screen外に存在したら、
                    self.rct.move_ip(((value[0] * (-1)), (value[1] * (-1))))   # 外に出ないように位置情報を更新する
        
        self.blit(sfc)   # 台を描く


class CPUTable:
    """ 
    敵台にまつわることを制御する
    """
    def __init__(self, x: int, y: int, vx: int, vy: int, color: tuple=(255, 255, 255)):
        """
        イニシャライザ
        color : 色のタプル(tuple)
        x : 初期x座標
        y : 初期y座標
        vx : x座標方向速度
        vy : y座標方向速度
        """
        self.vx, self.vy = vx, vy   # 速度
        self.color = color   # 台の色
        self.count = 1   # ボールとの接触回数を取得する
        self.v = 0   # 速度の変化量
         
        self.rct = pg.Rect(x, y, 10, 30)   # 敵台のRectオブジェクトを生成
        
    def blit(self, sfc: Screen):
        """ 
        Screenオブジェクトのインスタンス変数であるsfc(Surfaceクラス)のインスタンスのblitメソッドを呼び出す
        """
        pg.draw.rect(sfc.sfc, self.color, self.rct)   # 敵台を表示する
        
    def update(self, sfc: Screen, ball):
        """ 
        Ballの位置情報から敵台の位置情報を更新する
        ball : class Ball
        """
        if self.rct.colliderect(ball.rct):   # ボールと衝突したら
            self.count += 1   # 衝突カウントを数える
            
        if ball.rct.top >= self.rct.top:   # ballの位置が敵台よりも高い時
            self.vy = 2 + (self.count * 0.01)
            
        elif ball.rct.top <= self.rct.top:   # ballの位置が敵台よりも低い時
            self.vy = -2 + ((-1) * self.count * 0.01)
            
        self.rct.move_ip(self.vx, self.vy)   # 位置情報を更新する
        self.blit(sfc)
        

class Ball:
    def __init__(self, r: int, x: int, y: int, vx: int, vy: int, color: tuple = (255, 255, 255)):
        """ 
        イニシャライザ
        color : 色のタプル(tuple)
        r : 半径(int)
        vx : x軸変化量
        vy : y軸変化量
        """
        self.vx, self.vy = vx, vy   # 速度
        self.color = color   # ボールの色
        self.r = r   # ボールの半径
        self.count = 0   # ボールと台の衝突回数
        
        self.sfc = pg.Surface((r*2, r*2))   # Bomb用のSurface
        self.rct = self.sfc.get_rect()
        self.rct.centerx, self.rct.centery = x, y   # 初期位置を画面サイズ中央にセットする
    
    def blit(self, sfc: Screen):
        """ 
        描く
        """
        pg.draw.circle(sfc.sfc, self.color, (self.rct.centerx, self.rct.centery), self.r)   # ボール(円)を描く
        
    def update(self, s_sfc: Screen, table_list: list[MyTable, CPUTable]):
        """ 
        Ballの制御を制御する
        """
        self.vx *= check_bound(self.rct, s_sfc.rct)[0]   # 画面端に接触した時に速度を反転させる
        self.vy *= check_bound(self.rct, s_sfc.rct)[1]
        
        if self.rct.collidelist(table_list) != -1:   # 台に接触した時
            self.count += 1   # 接触カウントを増加させる
            v = -1 + ((-1) * self.count * 0.01)   
            self.vx *= v   # 速度を変化させる
            
        if game_over(self.rct, s_sfc.rct) == True:   # ゲームオーバー(画面左右端に到達)の時
            setup()   # もう一度初期化する
        
        self.rct.move_ip(self.vx, self.vy)   # 位置情報を更新する
        self.blit(s_sfc)    # 表示


def get_event_queue():
    """ 
    eventqueueを取得し、取得状態を更新する
    """
    global key_list
    key_list = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()   # 2. ×ボタンが押された時の処理
                
        if event.type == pg.KEYDOWN:       # キーを押したとき
            if event.key == pg.K_ESCAPE:   # Escキーが押されたとき
                pg.quit()
                sys.exit()
            

def check_bound(obj_rct: pg.Rect, scr_rct: Screen):
    """
    obj_rctがscr_rct内に存在するかを判定する
    obj_rct : Brid rect_objもしくは、Bomb rect_obj
    scr_rct : Screen rect_obj
    """
    yoko, tate = +1, +1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def game_over(obj_rct: pg.Rect, scr_rct: pg.Rect):
    """ 
    画面の左右端に衝突したかを判定する
    """
    global my_score, ene_score
    if obj_rct.left < scr_rct.left:   # 左端に到達した時
        ene_score += 1   # 敵のスコアを増加させる
        return True
        
    elif scr_rct.right < obj_rct.right:   # 右端に到達した時
        my_score += 1   # 味方のスコアを増加させる
        return True
    return False


def time_count():
    global time
    time += 1   # 経過時間を増加させる
    font = pg.font.Font(None, 50)
    t_time = f"{time}"
    text_time = font.render(t_time, True, (255, 255, 255))
    screen.sfc.blit(text_time, (1, 1))   # 経過時間を表示する
    
    t_my_score, t_ene_score = f"{my_score}", f"{ene_score}"
    text_my_score, text_ene_score = font.render(t_my_score, True, (255, 255, 255)), font.render(t_ene_score, True, (255, 255, 255))
    screen.sfc.blit(text_my_score, (size[0]/2, 1))   # 味方のスコアと敵のスコアを表示する
    screen.sfc.blit(text_ene_score, (size[0]/2 + 50, 1))
    

def setup():
    global screen, size, my_table, ene_table, ball, time, key_list, my_score, ene_score
    size = (1200, 600)   # 画面サイズ
    MY_X, MY_Y, MY_VX, MY_VY = 40, size[1] // 2, 0, 2
    ENE_X, ENE_Y, ENE_VX, ENE_VY = size[0] - 40, size[1] // 2, 0, 2
    BALL_X, BALL_Y, BALL_R = size[0] // 2, size[1] // 2, 10
    
    if my_score > ene_score:
        BALL_VX, BALL_VY = 2, random.choice([-2, 2])
    
    elif my_score < ene_score:
        BALL_VX, BALL_VY = -2, random.choice([-2, 2])
        
    elif my_score == ene_score:
        BALL_VX, BALL_VY = random.choice([-2, 2]), random.choice([-2, 2])
    
    screen = Screen("ホッケー", size[0], size[1])   # スクリーンを呼び出す
    my_table = MyTable(MY_X, MY_Y, MY_VX, MY_VY)   # 味方台を呼び出す
    ene_table = CPUTable(ENE_X, ENE_Y, ENE_VX, ENE_VY)   # 敵台を呼び出す
    ball = Ball(BALL_R, BALL_X, BALL_Y, BALL_VX, BALL_VY)   # ボールを呼び出す
    time = 1


if __name__ == "__main__":
    pg.init()
    my_score, ene_score = 0, 0   # スコアを設定する
    setup()   # 初期設定を行う
    
    while True:
        clock_obj = pg.time.Clock()
        get_event_queue()   # イベントキューを取得する
        screen = Screen("ホッケー", size[0], size[1])   # 更新する
        
        my_table.update(screen)   # 味方台を更新する
        ene_table.update(screen, ball)   # 敵台を更新する
        ball.update(screen, [my_table.rct, ene_table.rct])   # ボールを更新する
        
        time_count()   # 時間表示とスコア表示を行う
        pg.display.update()
        clock_obj.tick(60)