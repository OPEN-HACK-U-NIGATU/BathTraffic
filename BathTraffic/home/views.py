from django.shortcuts import render
from django.http import JsonResponse
import os, sqlite3, datetime
import pandas as pd
from prophet import Prophet
from django.views.decorators.csrf import csrf_exempt
from google.cloud import vision

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

    # 予測結果をJSON形式に変換
    forecast1_json = forecast1[['ds', 'yhat']].to_json(orient='records', date_format='iso')
    forecast2_json = forecast2[['ds', 'yhat']].to_json(orient='records', date_format='iso')



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

def localize_objects(path):
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    c = 0

    for object_ in objects:
        if object_.name == "Shoe":
            c += 1

    return c

count = 0

@csrf_exempt
def get_img(request):
    if request.method == "POST":
        global count
        image = request.FILES["image"]
        now = datetime.datetime.now()
        image_path = os.path.join("home/image", now.strftime("%Y%m%d_%H%M") + ".jpg")
        with open(image_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)

        count = localize_objects(image_path)
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "error"})
