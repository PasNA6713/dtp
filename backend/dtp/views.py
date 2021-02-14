from collections import Counter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Dtp
from .serializers import DtpDetailSerializer, DtpCreateSerializer, DtpPointSerializer
from .filters import DtpFilter
from .services import get_dtps_by_ids, filter_range
from . import params


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


class GetPlotView(generics.ListAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DtpFilter

    def list(self, request, column, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        data = [dict(i).get(column) for i in serializer.data]
        new_data = []
        for point in data:
            if type(point) == list:
                new_data += point
            else:
                new_data.append(point)
        c = Counter(new_data)
        # c = {x: count for x, count in c.items() if count >= 5}
        return Response(c, status=200)
    

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
            'region': params.REGION,
            'category': params.CATEGORY
        })


class GetRangeDtps(generics.ListCreateAPIView):
    queryset = Dtp.objects.all()
    serializer_class = DtpPointSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DtpFilter

    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        all_points = [dict(i) for i in self.get_serializer(queryset, many=True).data]
        cur_point = {
            'lat': float(request.data.get('lat')),
            'long': float(request.data.get('long'))
        }
        data = filter(lambda x: filter_range(cur_point, x, 0.01), all_points)
        return Response(data, status=200)