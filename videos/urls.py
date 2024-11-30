from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<str:video_name>/', views.video_detail, name='video_detail'),
]