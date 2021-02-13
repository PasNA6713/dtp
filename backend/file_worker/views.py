from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .services import get_file
from dtp.services import fill_db_from_json


FILES = dict()

class UploadFileView(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']
        fill_db_from_json(file)
        return Response(status=status.HTTP_200_OK)


class CreateFileView(APIView):
    def post(self, request):
        params = request.data.get('params')
        if params is None: 
            return Response(
                {
                    "params": "Field is required",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if FILES:
            key = list(FILES.keys())[-1]+1
        else:
            key = 1
        FILES[key] = params
        return Response(key, status=200)


class DownloadFileView(APIView):
    def get(self, request, key, file_format):
        return get_file(file_format, FILES.pop(key))
