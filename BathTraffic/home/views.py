from django.shortcuts import render
from django.http import HttpResponse
import os

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

    # For test Front-end
    # return render(request, 'index.html', {
    #     "large": large,
    #     "small": small
    # })
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HttpResponse(html_content, content_type='text/html')