from django.shortcuts import render
from django.http import HttpResponse
import os

def home(request):
    # For test Front-end
    # return render(request, 'index.html')
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HttpResponse(html_content, content_type='text/html')
