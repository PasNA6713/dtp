from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Dtp
from .serializers import DtpSerializer, DtpCreateSerializer
from .filters import DtpFilter
from .services import fill_db_from_json
from . import params


class GetFilterParams(APIView):
    def get(self, request, format=None):
        return Response({
            'light': params.LIGHT,
            'weather': params.WEATHER,
            'nearby': params.NEARBY,
            'road_conditions': params.ROAD_CONDITIONS,
            'regions': params.REGIONS,
            'categories': params.CATEGORIES
        })


class UploadFileView(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']
        fill_db_from_json(file)
        return Response(status=status.HTTP_200_OK)


class DtpCreateView(generics.CreateAPIView):
    serializer_class = DtpCreateSerializer


class DtpDestroyView(generics.DestroyAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpSerializer


class DtpRetrieveView(generics.RetrieveAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpSerializer


class DtpListView(generics.ListAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DtpFilter