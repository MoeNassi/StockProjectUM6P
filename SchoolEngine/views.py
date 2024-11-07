from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import *
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import *
from .permissions import *

class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return School.objects.all()
        else:
            return School.objects.filter(id=self.request.user.school.id)

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminOrReadOnly]

class StocksPerSchoolViewSet(ModelViewSet):
    serializer_class = StockPerSchoolSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['stock__DeviceName']

    def create(self, request, *args, **kwargs):
        serializer = StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_instance = serializer.save()
        school_instance = get_object_or_404(School, id=self.kwargs['school_pk'])
        StocksPerSchool.objects.create(school=school_instance, stock=stock_instance)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.school.id == self.kwargs['school_pk'] or self.request.user.is_superuser:
            return StocksPerSchool.objects.filter(school_id=self.kwargs['school_pk'])
        else:
            return StocksPerSchool.objects.none()
    
    def get_serializer_context(self):
        return {'school_id': self.kwargs['school_pk']}

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT' and self.request.user.is_superuser:
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)