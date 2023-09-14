import sqlite3
import random
from datetime import datetime, timedelta

# データベースに接続
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 削除したいテーブルの名前を指定してテーブルを削除
table_name = 'bath_number'
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# テーブルを作成
cursor.execute('''CREATE TABLE IF NOT EXISTS bath_number (
                    ds TEXT,
                    big_number REAL,
                    small_number REAL
                )''')

# トランザクションを開始
conn.execute('BEGIN')

# 開始日時と終了日時を設定
start_date = datetime(2020, 1, 10, 16, 0, 0)
end_date = datetime(2022, 12, 26, 0, 0, 0)

# 1時間ごとのデータを生成して挿入
delta = timedelta(hours=1)
current_date = start_date

while current_date < end_date:
    if current_date.hour >= 16 and current_date.hour <= 18:
        ds = current_date.strftime('%Y-%m-%d %H:%M:%S')
        # ここでデータを生成（例：ランダムな浮動小数点数）
        big_number = random.randint(1,5)  # ここでデータを生成するコードを追加
        small_number = random.randint(1,3)
        cursor.execute("INSERT INTO bath_number (ds, big_number, small_number) VALUES (?, ?, ?)", (ds, big_number, small_number))

    elif current_date.hour >= 19 and current_date.hour <= 21:
        ds = current_date.strftime('%Y-%m-%d %H:%M:%S')
        big_number = random.randint(6,9)
        small_number = random.randint(3,5)
        cursor.execute("INSERT INTO bath_number (ds, big_number, small_number) VALUES (?, ?, ?)", (ds, big_number, small_number))

    elif current_date.hour >= 22 and current_date.hour <= 23:
        ds = current_date.strftime('%Y-%m-%d %H:%M:%S')
        big_number = random.randint(0,3)
        small_number = random.randint(0,2)
        cursor.execute("INSERT INTO bath_number (ds, big_number, small_number) VALUES (?, ?, ?)", (ds, big_number, small_number))
    current_date += delta

# データベース接続のクローズ
conn.commit()
conn.close()
