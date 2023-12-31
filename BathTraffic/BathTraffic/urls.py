from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    #Service Worker へのアクセス
    path('sw.js',
        (TemplateView.as_view(
            template_name="sw.js",
            content_type='application/javascript',
        )),
        name='sw.js'
    ),
]
