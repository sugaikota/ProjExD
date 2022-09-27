import random
import datetime
""" 
消えたアルファベットを探すゲーム
表示されるアルファベット文字の中で抜けている文字をさがすことを目的とする
表示されてから正解するまでの時間を競う
要件
1. 対象文字数、欠損文字数をグローバル変数として定義する
2. 対象文字はランダムな順序で表示する
3. 正解するまで繰り返し出題する。ただ、最大繰り返し回数をグローバル変数として定義する
4. プログラム実行から終了までの時間を計測し、表示する
5. 例外処理は必要ない
6. CUIで動くゲームにする
"""

global target_num, loss_num, max_act_num   #対象文字数、欠損文字数をグローバル変数として定義する.

def random_choice_alphabet(target_num, loss_num, max_act_num):
    num = 1
    while num <= max_act_num:
        all_alpha_list = [chr(i) for i in range(65, 91)]   #すべてのアルファベットが入ったlist
        target_alpha_list = random.sample(all_alpha_list, target_num)   #対象文字数から、ランダムに選んでくる
        loss_alpha_list = random.sample(target_alpha_list, (target_num - loss_num))   #欠損文字数から、ランダムに選んでくる
        
        target_alpha_set, loss_alpha_set = set(target_alpha_list), set(loss_alpha_list)
        loss_alpha = target_alpha_set - loss_alpha_set   #どの文字が欠損したかを保持する(type : set)
        
        print("対象文字 : ")   #対象文字列を表示する
        for i in target_alpha_list:
            print(i + " ", end = "")
            
        print()
        print("欠損文字 : ")   #欠損文字列を表示する
        for i in loss_alpha_list:
            print(i + " ", end = "")
            
        print()
        try :
            num_ans = int(input("欠損文字はいくつあるでしょうか : "))   #回答者の欠損文字数を保持
        
        except ValueError as e:
            num_ans = int(input("数字を入力してください : "))   #例外処理
        
        if num_ans == loss_num:   #欠損文字数の判定を行う
            print("正解です")
            print("それでは具体的に欠損文字を一つずつ入力してください")   #欠損文字の入力を促す
            ans_1 = input("一つ目の文字を入力してください : ")
            ans_2 = input("二つ目の文字を入力してください : ")
            
            if {ans_1, ans_2} == loss_alpha:   #もし二つとも正解ならば
                print("正解です")
                break
                
            else:   #正解でないならば
                if num >= max_act_num:
                    print("不正解です。これ以上チャレンジできません")
                else:
                    print("不正解です。またチャレンジしてください")
                    print("-" * 10)
            
        else:   #欠損文字数が異なれば
            if num >= max_act_num:
                print("不正解です。これ以上チャレンジできません")
            else:
                print("不正解です。またチャレンジしてください")
                print("-" * 10)
            
        num += 1
        
if __name__ == "__main__":
    target_num, loss_num, max_act_num = 10, 2, 5   #対象文字数、欠損文字数、最大繰り返し回数を保持しておく
    start_time = datetime.datetime.now()   #回答開始時間を保持する
    random_choice_alphabet(target_num, loss_num, max_act_num)   #アルファベットゲームを開始する
    finish_time = datetime.datetime.now()   #回答終了時間を保持する
    print(f"所要時間は{(finish_time - start_time).seconds}秒です。")   #所要時間を表示