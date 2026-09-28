import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
    
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs.save(file.name, file)
        return redirect('index')

    # Lista os arquivos existentes
    try:
        arquivos = fs.listdir('')[1]  # Retorna tupla (diretorios, arquivos)
    except Exception:
        arquivos = []

    return render(request, 'index.html', {'arquivos': arquivos})
