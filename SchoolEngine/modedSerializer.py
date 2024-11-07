from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import *

class UserCreateSerializer(BaseUserCreateSerializer):
    permission_classes = [IsAdminOrReadOnly]

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'school', 'password', 'is_superuser', 'is_staff']

class UserSerializer(BaseUserSerializer):
    permission_classes = [IsAdminOrReadOnly]

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']