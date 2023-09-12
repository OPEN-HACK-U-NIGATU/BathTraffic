from django.urls import path,include
from . import views
#画像を読み込み
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
]