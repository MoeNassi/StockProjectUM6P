from rest_framework import serializers
from .models import *

class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['id', 'Device']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'SerialNumber', 'DeviceType', 'HostName', 'Brand', 'Date', 'Model', 'Config', 'DeviceStatus',
                  'Garantie', 'Dotation', 'MiseEnRebute', 'NumeroArrivage', 'Retour']

class StockPerSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = StocksPerSchool
        fields = ['stock', 'date']

    def create(self, validated_data):
        school_id = self.context['school_id']
        return StocksPerSchool.objects.create(school_id=school_id, **validated_data)

    stock = StockSerializer()

class SchoolSerializer(serializers.ModelSerializer):
    capacity = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'name', 'devices', 'capacity', 'NBonLivraison']

    def get_capacity(self, obj):
        return f'{int(obj.devices.count())}'

    devices = StockPerSchoolSerializer(many=True, read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'school', 'email']
