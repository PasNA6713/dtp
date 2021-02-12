from rest_framework import serializers

from .models import Dtp


class DtpPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dtp
        fields = ['id', 'lat', 'long']

        
class DtpDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dtp
        fields = '__all__'


class DtpCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dtp
        fields = ['lat', 'long']