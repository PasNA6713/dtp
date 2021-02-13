import json
import os

from django.http import HttpResponse
from wsgiref.util import FileWrapper

import pandas as pd

from dtp.services import construct_data, get_model_fields


def construct_dataframe(params) -> pd.DataFrame:
    data = construct_data(params)
    d = []
    for claster in range(len(data)):
        for point in data[claster].get('points'):
            string = list(point.values())[1:] + [claster, data[claster].get('lat'), data[claster].get('long')]
            d.append(string)
    col = get_model_fields()
    return pd.DataFrame(data=d, columns=col)

def create_json_file(filename: str, params: dict) -> None:
    with open(filename, 'w') as outfile:
        json.dump({
            'clasters': construct_data(params)
        }, outfile, indent=4, ensure_ascii=False)

def create_csv_file(filename: str, params: dict) -> None:
    construct_dataframe(params).to_csv(filename, encoding='cp1251')

def create_xlsx_file(filename: str, params: dict) -> None:
    construct_dataframe(params).to_excel(filename)


def get_file(file_format: str, params: dict) -> HttpResponse:
    filename = f'data.{file_format}'
    
    if file_format == 'json':
        create_json_file(filename, params)
    if file_format == 'csv':
        create_csv_file(filename, params)
    if file_format == 'xlsx':
        create_xlsx_file(filename, params)

    with open(filename, 'rb') as short_report:
        # конструирование ответа
        content = f'application/{file_format}'
        response = HttpResponse(
                FileWrapper(short_report),
                content_type=content
            )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        os.remove(filename) # удаление файла
        return response
