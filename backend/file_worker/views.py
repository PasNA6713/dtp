import json

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .services import get_file
from dtp.services import fill_db_from_json


class UploadFileView(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']
        fill_db_from_json(file)
        return Response(status=status.HTTP_200_OK)


class CreateFileView(APIView):
    def post(self, request):
        params = request.data
        if params is None: 
            return Response(
                {
                    "params": "Field is required",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        with open('files.json', 'r') as json_file:
            files = json.load(json_file)
        if files:
            key = int(list(files.keys())[-1]) + 1
        else:
            key = 1
        files[key] = params
        with open('files.json', 'w') as outfile:
            json.dump(files, outfile)
        return Response(key, status=200)


class DownloadFileView(APIView):
    def get(self, request, key, file_format):
        with open('files.json') as json_file:
            files = json.load(json_file)
        file_info = files.pop(str(key))
        with open('files.json', 'w') as outfile:
            json.dump(files, outfile)
        return get_file(file_format, file_info)
