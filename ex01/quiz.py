import random
import datetime
""" 
練習1
クイズ問題3問とそ䛾正解をあらかじめ用意しておく
※表記ゆれを考慮するために，複数正解を用意する
• 3問中からランダムに1問出題する
•解答者の答えが正解or不正解かを出力する
•出題から解答までの時間を計測し，最後に所要時間を出力する
• CUIで動くゲームにする
問題 解答１ 解答２ 解答３ 解答４
サザエさんの旦那の名前は？ マスオ ますお
カツオの妹の名前は？ ワカメ わかめ
タラオはカツオから見てどんな関係？ 甥 おい 甥っ子 おいっこ
"""

def shuffle_quiz():
    """ 
    問題を選択し、それらを表示する. その後、回答者からの回答を受け取り、正誤判定及び、回答所要時間を表示する
    """
    quiz_1, quiz_2, quiz_3 = "サザエさんの旦那の名前は?", "カツオの妹の名前は?", "タラオはカツオから見てどんな関係?"   #問題文を保持
    quiz_1_ans, quiz_2_ans, quiz_3_ans = ["マスオ", "ますお"], ["ワカメ", "ワカメ"], ["甥", "おい", "甥っ子", "おいっこ"]   #問題文にあった回答を保持
    
    quiz_list = [quiz_1, quiz_2, quiz_3]   #各クイズの問題文を保持する(type : list)
    quiz_ans_list = [quiz_1_ans, quiz_2_ans, quiz_3_ans]   #各クイズの回答を保持する(type : list)
    
    random_num = random.randint(0, 2)   #クイズをランダムに決める乱数(type : int)
    print(quiz_list[random_num])   #ランダムに選んだクイズを表示する
    
    start_time = datetime.datetime.now()   #回答開始時間を保持する
    answer = input("回答 : ")   #回答者の回答を保持する(type : str)
    finish_time = datetime.datetime.now()
    
    judge = "あなたの回答は不正解です。"   #回答結果を保持する変数(type : str)
    if (answer in quiz_ans_list[random_num]) == True:
        judge = "あなたの回答は正解です。"   #回答結果を正解に変更する
            
    print(judge)   #回答結果を表示
    print(f"所要時間は{(finish_time - start_time).seconds}秒です。")   #所要時間を表示
    
    
if __name__ == "__main__":
    shuffle_quiz()