from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
import os
import mimetypes
from wsgiref.util import FileWrapper
import re

# Regex para processar o cabeçalho range
range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)

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

def stream_video(request, video_name):
    """Função para streaming otimizado de vídeo"""
    path = os.path.join(settings.VIDEOS_DIR, video_name)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    chunk_size = 8192  # 8KB por chunk
    
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        length = last_byte - first_byte + 1
        
        resp = StreamingHttpResponse(
            file_iterator(path, chunk_size, first_byte, length),
            status=206,
            content_type=mimetypes.guess_type(path)[0]
        )
        resp['Content-Length'] = length
        resp['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'
    else:
        resp = StreamingHttpResponse(
            FileWrapper(open(path, 'rb'), chunk_size),
            content_type=mimetypes.guess_type(path)[0]
        )
        resp['Content-Length'] = size
    
    resp['Accept-Ranges'] = 'bytes'
    resp['Cache-Control'] = 'public, max-age=36000'  # Cache por 10 horas
    
    return resp

def file_iterator(path, chunk_size, start=0, length=None):
    """Função auxiliar para iterar sobre o arquivo em chunks"""
    with open(path, 'rb') as file:
        file.seek(start)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = file.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data