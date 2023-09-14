import pandas as pd
from prophet import Prophet
import sqlite3

conn = sqlite3.connect('BathTraffic\db.sqlite3')

query = 'SELECT * FROM bath_number;'
df = pd.read_sql_query(query,conn)

# Prophetモデルの初期化
model = Prophet()

# データのカラム名をds（日付）とy（目的変数）に変更
df.rename(columns={'ds': 'ds', 'big_number': 'y'}, inplace=True)

# モデルにデータをフィット
model.fit(df)

# 予測を生成
future = model.make_future_dataframe(periods=365)  # 予測期間を指定
future.tail()

forecast = model.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()



fig1 = model.plot(forecast)

fig1.show()
input("Press Enter to close the plot...")