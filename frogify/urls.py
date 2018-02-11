from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('queue', views.queue, name='queue'),
    path('redirect_login', views.redirect_login, name='redirect_login')
]
