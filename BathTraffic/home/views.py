from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
from prophet import Prophet
import sqlite3
from datetime import datetime, timedelta

def home(request):
    # 簡単な色変更用のプログラムを追加しました。
    large = {"count": 7}
    small = {"count": 2}
    large_color = ""
    small_color = ""

    if large["count"] >= 0 and large["count"] < 4:
        large_color = "green"
    elif large["count"] >= 4 and large["count"] < 7:
        large_color = "yellow"
    else:
        large_color = "red"
    if small["count"] >= 0 and small["count"] < 3:
        small_color = "green"
    elif small["count"] >= 3 and small["count"] < 5:
        small_color = "yellow"
    else:
        small_color = "red"
        
    large["color"] = large_color
    small["color"] = small_color

    #ここから予測部分
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
    # start_time = today + timedelta(hours=16)
    # end_time = today + timedelta(hours=23)
    start_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)
    forecast_hours = (end_time - start_time).seconds // 3600 + 1

     # 1時間ごとの日付を生成
    date_list = [start_time + timedelta(hours=i) for i in range(forecast_hours)]
    
    # 予測期間を指定
    future1 = pd.DataFrame({'ds': date_list})
    # future1 = bigmodel.make_future_dataframe(periods=7,freq='H') 
    # future1 = future1[(future1['ds'] >= start_time) & (future1['ds'] <= end_time)]
    # future1['ds'] = pd.date_range(start=start_time,end=end_time,freq='H')
    future1.tail()

    future2 = pd.DataFrame({'ds': date_list})
    # future2 = smallmodel.make_future_dataframe(periods=7,freq='H')
    # future2 = future1[(future2['ds'] >= start_time) & (future2['ds'] <= end_time)] 
    # future2['ds'] = pd.date_range(start=start_time,end=end_time,freq='H')
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

    print(forecast1_json)
    return render(request, 'index.html', {
        "large": large,
        "small": small,
        "forecast1_json":forecast1_json,
        "forecast2_json":forecast2_json,
    })

'''
#グラフ用の関数
# views.py
from django.shortcuts import render
from .models import YourModel

def chart_view(request):
    # データベースから時間帯と人数を取得する処理
    time_labels = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]  # 時間帯のラベルリスト
    small_data = ["2", "3", "4", "5", "6", "7", "8", "9"]   # 小風呂の人数データ
    large_data = ["2", "3", "4", "5", "6", "7", "8", "9"]   # 大風呂の人数データ

    context = {
        'time_labels': time_labels,
        'small_data': small_data,
        'large_data': large_data,
    }

    return render(request, 'index.html', context)
'''