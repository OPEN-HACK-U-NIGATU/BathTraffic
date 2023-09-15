from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
from prophet import Prophet
import sqlite3
from datetime import datetime, timedelta

def periodic_execution():# 任意の関数名
    # ここに定期実行したい処理を記述する
    conn = sqlite3.connect('db.sqlite3')

    query = 'SELECT * FROM bath_number;'
    df1 = pd.read_sql_query(query,conn)
    df2 = pd.read_sql_query(query,conn)

    # Prophetモデルの初期化
    bigmodel = Prophet()
    smallmodel = Prophet()

    # データのカラム名をds（日付）とy（目的変数）に変更
    df1.rename(columns={'ds': 'ds', 'big_number': 'y'}, inplace=True)
    df2.rename(columns={'ds': 'ds', 'small_number': 'y'}, inplace=True)

    # モデルにデータをフィット
    bigmodel.fit(df1)
    smallmodel.fit(df2)

    # 予測を生成
    # 今日の日付を取得
    now = datetime.now()

    # 今日の16:00を開始時刻とし、23:00を終了時刻とする時間帯を生成
    start_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)
    forecast_hours = (end_time - start_time).seconds // 3600 + 1

    # 1時間ごとの日付を生成
    date_list = [start_time + timedelta(hours=i) for i in range(forecast_hours)]
    
    # 予測期間を指定
    future1 = pd.DataFrame({'ds': date_list})
    future1.tail()

    future2 = pd.DataFrame({'ds': date_list})
    future2.tail()


    forecast1 = bigmodel.predict(future1)
    forecast1[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    forecast2 = smallmodel.predict(future2)
    forecast2[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


    # fig1 = bigmodel.plot_components(forecast1)
    # fig2 = smallmodel.plot_components(forecast2)

    # fig1.show()
    # fig2.show()
    # input("Press Enter to close the plot...")

    # 予測結果をJSON形式に変換
    forecast1_json = forecast1[['ds', 'yhat']].to_json(orient='records', date_format='iso')
    forecast2_json = forecast2[['ds', 'yhat']].to_json(orient='records', date_format='iso')


    #テーブルの削除
    cursor = conn.cursor()
    table_name = 'forecast_data'
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")


    # テーブルを作成
    cursor.execute('''CREATE TABLE IF NOT EXISTS forecast_data (
                        big_forecast_json JSON,
                        small_forecast_json JSON
                    )''')

    # トランザクションを開始
    conn.execute('BEGIN')

    # SQLiteデータベースにJSONデータを挿入
    cursor = conn.cursor()
    cursor.execute("INSERT INTO forecast_data (big_forecast_json, small_forecast_json) VALUES (?, ?)", (forecast1_json, forecast2_json))

    # トランザクションをコミット
    conn.commit()

    # データベース接続を閉じる
    conn.close()

    print ("定期実行")
    
        
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'cron', hour=0, minute=0)# 毎日0時0分に実行
    scheduler.start()