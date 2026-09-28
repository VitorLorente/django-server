from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from server.views import index, deletar_arquivo, editar_arquivo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    
    # Novas rotas de manipulação
    path('deletar/<str:nome_arquivo>/', deletar_arquivo, name='deletar_arquivo'),
    path('editar/<str:nome_arquivo>/', editar_arquivo, name='editar_arquivo'),
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
