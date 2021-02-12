from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from dtp.models import Dtp
from dtp.filters import DtpFilter

from .clasterization import claster
from .serializers import DtpClasterSerializer


class GetClastersView(generics.ListAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpClasterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DtpFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
