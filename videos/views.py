from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator  # Adicione esta linha
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
    """Lista todos os vídeos da pasta com paginação"""
    # Pega a lista completa de vídeos
    videos = get_videos()
    
    # Cria um objeto de paginação com 9 itens por página
    paginator = Paginator(videos, 9)
    
    # Pega o número da página da URL (?page=1)
    page_number = request.GET.get('page', 1)
    
    # Obtém os objetos da página atual
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'videos/video_list.html', {
        'videos': page_obj.object_list,  # Lista de vídeos da página atual
        'page_obj': page_obj  # Objeto de paginação completo
    })

def video_detail(request, video_name):
    """Mostra um vídeo específico"""
    videos = get_videos()
    video = next((v for v in videos if v['file'] == video_name), None)
    return render(request, 'videos/video_detail.html', {'video': video})
