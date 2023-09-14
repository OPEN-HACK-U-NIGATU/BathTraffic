import pandas as pd
from prophet import Prophet
import sqlite3

conn = sqlite3.connect('BathTraffic/db.sqlite3')

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
future1 = bigmodel.make_future_dataframe(periods=365*24,freq='H')  # 予測期間を指定
future1.tail()

future2 = smallmodel.make_future_dataframe(periods=365*24,freq='H')  # 予測期間を指定(freq='H'で一時間ごとに予測)
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

cursor = conn.cursor()

table_name = 'forecast_data'
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")


# テーブルを作成
cursor.execute('''CREATE TABLE IF NOT EXISTS forecast_data (
                    Bmodel TEXT,
                    big_forecast_json TEXT,
                    Smodel TEXT,
                    small_forecast_json TEXT
                )''')

# トランザクションを開始
conn.execute('BEGIN')

# 予測結果をJSON形式に変換
forecast1_json = forecast1[['ds', 'yhat']].to_json(orient='records', date_format='iso')
forecast2_json = forecast2[['ds', 'yhat']].to_json(orient='records', date_format='iso')

print(forecast1_json)

# SQLiteデータベースにJSONデータを挿入
cursor = conn.cursor()
cursor.execute("INSERT INTO forecast_data (Bmodel, big_forecast_json, Smodel, small_forecast_json) VALUES (?, ?, ?, ?)", ('bigmodel', forecast1_json, 'smallmodel', forecast2_json))

# トランザクションをコミット
conn.commit()

# データベース接続を閉じる
conn.close()