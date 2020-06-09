from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name='ImageClassificationApp'

urlpatterns=[
    path('home', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('', views.logout_user, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)