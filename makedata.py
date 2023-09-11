import sqlite3
import random

# データベースに接続
conn = sqlite3.connect('BathTraffic\db.sqlite3')
cursor = conn.cursor()

# テーブルの作成SQL文を定義
create_table_sql = '''CREATE TABLE bath_number (
                        id INTEGER PRIMARY KEY,
                        month INTEGER NOT NULL,
                        day INTEGER NOT NULL,
                        hour INTEGER NOT NULL,
                        small_number INTEGER NOT NULL,
                        big_number INTEGER NOT NULL
                    )'''

# テーブルの作成SQL文を実行
cursor.execute(create_table_sql)

# トランザクションを開始
conn.execute('BEGIN')

# 1月から12月までの各月について繰り返し
for month in range(1, 13):
    # 各月の各日について繰り返し
    for day in range(1, 32):
        # 各時間帯の入場者数をランダムに生成（16:00から23:00まで）
        for hour in range(16, 24):
            small_number = random.randint(0, 10)  # 少人数用浴場の入場者数
            big_number = random.randint(0, 20)   # 大人数用浴場の入場者数

            # データを挿入
            insert_sql = 'INSERT INTO bath_number (month, day, hour, small_number, big_number) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(insert_sql, (month, day, hour, small_number, big_number))


# データベース接続のクローズ
conn.commit()
conn.close()
