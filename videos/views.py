from django.shortcuts import render
from django.conf import settings
import os

def get_videos():
    """Busca todos os vídeos na pasta configurada"""
    videos = []
    for file in os.listdir(settings.VIDEOS_DIR):
        if any(file.lower().endswith(ext) for ext in settings.VIDEO_EXTENSIONS):
            name = os.path.splitext(file)[0].replace('_', ' ').title()
            videos.append({
                'name': name,
                'file': file,
                'path': os.path.join('videos_folder', file)
            })
    return sorted(videos, key=lambda x: x['name'])

def video_list(request):
    """Lista todos os vídeos da pasta"""
    videos = get_videos()
    return render(request, 'videos/video_list.html', {'videos': videos})

def video_detail(request, video_name):
    """Mostra um vídeo específico"""
    videos = get_videos()
    video = next((v for v in videos if v['file'] == video_name), None)
    return render(request, 'videos/video_detail.html', {'video': video})
# Create your views here.
