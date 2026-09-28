import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Helper para pegar o caminho correto da pasta de uploads
def get_upload_path():
    return os.path.join(settings.MEDIA_ROOT, 'uploads')


@login_required
def index(request):
    fs = FileSystemStorage(location=get_upload_path())
    
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs.save(file.name, file)
        return redirect('index')

    try:
        # Garante pegar apenas os nomes dos arquivos na lista
        _, arquivos = fs.listdir('')
    except Exception:
        arquivos = []

    return render(request, 'index.html', {'arquivos': sorted(arquivos)})


@login_required
def deletar_arquivo(request, nome_arquivo):
    if request.method == 'POST':
        caminho_arquivo = os.path.join(get_upload_path(), nome_arquivo)
        
        # Segurança básica: impede manipulação de caminhos com '../'
        if os.path.exists(caminho_arquivo) and os.path.commonpath([get_upload_path(), caminho_arquivo]) == get_upload_path():
            os.remove(caminho_arquivo)
            
    return redirect('index')


@login_required
def editar_arquivo(request, nome_arquivo):
    caminho_antigo = os.path.join(get_upload_path(), nome_arquivo)
    
    # Valida se o arquivo de fato existe
    if not os.path.exists(caminho_antigo):
        raise Http404("Arquivo não encontrado")

    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome', '').strip()
        
        if novo_nome:
            # Mantém a extensão original caso o usuário não digite
            _, extensao_original = os.path.splitext(nome_arquivo)
            _, extensao_nova = os.path.splitext(novo_nome)
            
            if not extensao_nova:
                novo_nome += extensao_original
                
            caminho_novo = os.path.join(get_upload_path(), novo_nome)
            
            # Renomeia se o arquivo de destino não existir
            if not os.path.exists(caminho_novo):
                os.rename(caminho_antigo, caminho_novo)
                
        return redirect('index')

    return render(request, 'editar.html', {'nome_arquivo': nome_arquivo})
