from django.shortcuts import render
from django.http import JsonResponse
import os
import sqlite3
import ast

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

    #予測情報
    # データベースに接続
    conn = sqlite3.connect('db.sqlite3')
    # カーソルを作成
    cursor = conn.cursor()
    # SQLクエリを実行
    cursor.execute('SELECT big_forecast_json FROM forecast_data;')
    forecast1_json = cursor.fetchall()

    cursor.execute('SELECT small_forecast_json FROM forecast_data;')
    forecast2_json = cursor.fetchall()

    # クエリの後片付け
    cursor.close()
    conn.close()

    forecast1_list = ast.literal_eval(forecast1_json[0][0])
    forecast2_list = ast.literal_eval(forecast2_json[0][0])
    # return JsonResponse(forecast1_list, safe=False)
    forecastS = []
    forecastL = []
    for row in forecast1_list:
        forecastL.append(row['yhat'])
    for row in forecast2_list:
        forecastS.append(row['yhat'])

    return render(request, 'index.html', {
        "large": large,
        "small": small,
        "forecastS": forecastS,
        "forecastL": forecastL,
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