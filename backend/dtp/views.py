from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Dtp
from .serializers import DtpDetailSerializer, DtpCreateSerializer, DtpPointSerializer
from .filters import DtpFilter
from .services import get_dtps_by_ids
from . import params


class GetSomeDtps(APIView):
    def post(self, request, format=None):
        ids = request.data.get('ids')
        if ids is None: return Response(
            {"Detail": "Field 'ids' is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        data = DtpDetailSerializer(get_dtps_by_ids(ids), many=True).data
        return Response(
            data,
            status=status.HTTP_200_OK
        )


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


class DtpCreateView(generics.CreateAPIView):
    serializer_class = DtpCreateSerializer


class DtpDestroyView(generics.DestroyAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpPointSerializer


class DtpRetrieveView(generics.RetrieveAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpDetailSerializer


class DtpListView(generics.ListAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpPointSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DtpFilter

