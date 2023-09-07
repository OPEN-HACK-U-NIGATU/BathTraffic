from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    with open('home/templates/index.html','r') as f:
        html_content = f.read()
    return HttpResponse(html_content,content_type='text/html')