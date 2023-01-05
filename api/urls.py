from django.contrib import admin
from django.urls import path, include

#ninja api
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import JsonResponse
from api.apiutils import find_latest_file
import csv
import json
import pandas as pd
from .models import ChessOpening

api = NinjaAPI()

@api.get('/opening')
def get_opening(request, move:str):
  payload = [{'move' : 'e2e4', 'name':'test.name', 'wdl' : 'testwdl'},{'move' : 'e2e4', 'name':'test.name', 'wdl' : 'testwdl'}]
  return JsonResponse(payload, safe=False)

@api.post('/opening')
def store_opening_data(request, uploaded_file: UploadedFile = File(...)):
  # UploadedFile is an alias to Django's UploadFile
    with open(f'api\\dist\\data\\{uploaded_file.name}', 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return uploaded_file.name

@api.get('/opening/to_data')
def to_database(request, filename:str):
    data = pd.read_csv(f"api\\dist\\data\\{filename}")
    ChessOpening.objects.all().delete()

    for i in data.index:
      if data.loc[i, 'Move'] == 'start':
        op = ChessOpening(i, data.loc[i,'Move'], data.loc[i,'Next Moves'], data.loc[i, 'Opening Name'])
      else:
        op = ChessOpening(i, ','.join(eval(data.loc[i,'Move'])), data.loc[i,'Next Moves'], data.loc[i, 'Opening Name'])
      op.save()


urlpatterns = [
    path('api/', api.urls),
]
