# 第3回
## 迷路作成(maze.py)
### 追加機能
- ゴールの位置に到達すると、ポップアップが表示され、1秒後にプログラムが終了する.
- 一定時間ごとに、動く障害物を導入し、接触するとスタート位置に戻され、ポップアップが表示される
- 
### ToDo（実装しようと思ったけど時間がなかった）
- 障害物が壁の中も移動するため、初期位置の設定と、自キャラが動く関数を更新し、同時に二つのオブジェクトを動かせるようにする
- スタートの位置と、ゴールの位置のみ、色を変化させる。
- 障害物がポップアップ中にも動き続ける.
### メモ
- after関数で呼んだ関数の中に、再びafter関数を呼び出すことで、再帰的に関数を呼び出すことが出来る.