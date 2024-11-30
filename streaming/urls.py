from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videos.urls')),  # não inclua o mesmo arquivo duas vezes
]

# Adicione esta linha no final do arquivo
if settings.DEBUG:
    urlpatterns += static('/videos_folder/', document_root=settings.VIDEOS_DIR)