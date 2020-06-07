from django.urls import path
from . import views


app_name='imagefilters'

urlpatterns=[
    path('home', views.home_page, name='home_page'),
]