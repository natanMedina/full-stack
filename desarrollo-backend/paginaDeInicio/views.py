from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.decorators import action

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from datetime import timezone
from rest_framework.exceptions import AuthenticationFailed  # Import added
from rest_framework.permissions import AllowAny

from .models import Usuario, Rol, Task
from .serializers import UsuarioSerializer, TaskSerializer



class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        usuario = request.data.get('usuario')
        password = request.data.get('contrasena')

        try:
            # Buscar al usuario por nombre de usuario en la base de datos
            usuario_obj = Usuario.objects.get(username=usuario)

            # Verificar la contraseña del usuario
            if usuario_obj.check_password(password):
                print(f"Información del usuario: {user_data}")
                # Autenticar al usuario y generar un token de autenticación
                user = authenticate(username=usuario, password=password)
                if user is not None:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)

                    user_data = {
                        'id': user.id,
                        'documento': usuario_obj.nro_identificacion,
                        'nombre': usuario_obj.get_full_name(),
                        'tipo_identificacion': usuario_obj.tipo_identificacion,
                        'genero': usuario_obj.genero,
                        'direccion': usuario_obj.direccion,
                        'celular': usuario_obj.celular,
                        'rol': usuario_obj.rol.nombre,
                        'foto_perfil': usuario_obj.fotografia.url if usuario_obj.fotografia else None,
                    }

                    return Response({'valid': True, 'token': token.key, **user_data})

            raise AuthenticationFailed('Las credenciales proporcionadas son inválidas.')

        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Las credenciales proporcionadas son inválidas.')

        return Response({'valid': False})



class GerentePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.rol.nombre == 'Gerente':
            return True
        return False



class UsuarioViewSet(viewsets.ModelViewSet):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer
   permission_classes = []
   
   @action(detail=True, methods=['get'])
   def get_name(self, request, pk=None):
    usuario = self.get_object()
    nombre = usuario.get_full_name()  # Suponiendo que get_full_name devuelve el nombre
    return Response(nombre)  # Devuelve el nombre envuelto en una respuesta DRF



class TaskView(viewsets.ModelViewSet):
   serializer_class = TaskSerializer
   queryset = Task.objects.all()