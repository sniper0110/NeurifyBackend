from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name='ImageClassificationApp'

urlpatterns=[
    path('home', views.home, name='home_page'),
    path('home/image_classification', views.adding_task, name='adding_new_task'),
    path('home/image_classification/<str:pk>', views.adding_imageclass, name='image_classes_task'),
    path('home/image_classification/<str:pk1>/<str:pk2>', views.adding_images, name='upload_images'),
    path('home/classification_training', views.classification_training, name='classification_training'),
    path('home/image/classification/history', views.history_page, name='history_page'),
    path('home/classification/pretraining/summary', views.pretraining_summary, name='pretraining_summary'),
    path('home/classification/training/progress', views.training_progress_and_result, name='training_progress'),
    path('', views.download_trained_model, name='download_trained_model'),

    path('api/data/training/history/', views.training_history_data, name='training_history_data'),

    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('', views.logout_user, name='logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)