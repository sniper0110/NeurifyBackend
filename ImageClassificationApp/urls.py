from django.urls import path
from . import views


app_name='ImageClassificationApp'

urlpatterns=[
    path('home', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),

]