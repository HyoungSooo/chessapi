from django.contrib import admin
from django.urls import path, include

#ninja api
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import JsonResponse
from api.apiutils import find_latest_file, get_stock_fish
import csv
import json
import pandas as pd
from .models import ChessOpening

api = NinjaAPI()

@api.get('/opening')
def get_opening(request, move:str):
  obj = ChessOpening.objects.get(move =move)
  data = {'next_move':obj.next_move.split(','), 'name' : obj.name}
  return JsonResponse(data) 

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

@api.get('/stockfish')
def ask_to_stockfish(request, fen:str):
  try:
    stockfish = get_stock_fish()

    if stockfish.is_fen_valid(fen):
      stockfish.set_fen_position(fen)
      ans = stockfish.get_top_moves(5)

      return JsonResponse(ans, safe=False)
    else:
      msg = {'msg': 'fen is unvaild'}
      return JsonResponse(msg)

  except:
    msg = {'msg' : 'stockfish load error plz try later'}
    return JsonResponse(msg)

  

urlpatterns = [
    path('api/', api.urls),
]
