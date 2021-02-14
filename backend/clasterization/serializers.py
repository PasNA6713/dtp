from rest_framework import serializers

from dtp.models import Dtp


class DtpClasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dtp
        fields = ['id', 'lat', 'long', 'region', 'address']