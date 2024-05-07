from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from paginaDeInicio.views import UsuarioViewSet, LoginView, buscar_usuarios, inhabilitar_usuario, habilitar_usuario, createUserView, updateView


from crud.views import WorkViewSet


from django.conf import settings
from django.conf.urls.static import static

#ola laura 
#ola satanas ----fvgb h fdaf 

router = routers.DefaultRouter()
router.register('api/users', UsuarioViewSet, 'nombra_urls_usuarios')
router.register('api/obras', WorkViewSet)


urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include(router.urls)),

  #Urls del Usuario
  path('api/users/<int:pk>/name/', UsuarioViewSet.as_view({'get': 'get_name'})),
  path('login/', LoginView.as_view()),

  #URLS DEL CRUD
  #create
  path('crear-usuario/', createUserView.as_view()),
  #read
  path('api/usuarios/buscar/', buscar_usuarios.as_view()),
  #update
  path('update-usuario/', updateView.as_view()),

  #delete
  path('inhabilitar/', inhabilitar_usuario.as_view()),
  path('habilitar/', habilitar_usuario.as_view()),


  #Urls de las obras
  path('api/obras/por-director/{id_director}/', WorkViewSet.as_view({'get': 'filtrar_por_director'})),

  #URLS DEL CRUD
  #create
  #read
  #updateS
  #delete
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)