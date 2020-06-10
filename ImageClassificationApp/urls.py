from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name='ImageClassificationApp'

urlpatterns=[
    path('home', views.home, name='home_page'),
    path('home/image_classification', views.image_classification_content, name='image_classification'),
    path('home/image_classification/<str:pk>', views.image_classes_task, name='image_classes_task'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('', views.logout_user, name='logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)