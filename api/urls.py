from django.contrib import admin
from django.urls import path, include

#ninja api
from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile
from django.http import JsonResponse
from api.apiutils import find_latest_file, get_stock_fish, eval_position
import csv
import json
import pandas as pd
from .models import ChessOpening
from stockfish import StockfishException
import chess


api = NinjaAPI()

@api.get('/opening')
def get_opening(request, move:str):
  try:
    obj = ChessOpening.objects.get(move =move)
  except:
    msg = {'msg' : 'There is no related opening data'}
    return JsonResponse(msg)
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

@api.get('/getfen')
def get_fen_position_by_moves(request, move:str):
  try:
    stockfish = get_stock_fish()
    moves = move.split(',')
    stockfish.set_position(moves)
    ans = {'fen': stockfish.get_fen_position()}
    return JsonResponse(ans)
  except ValueError:
    msg = {'msg': 'unvalid move'}
    return JsonResponse(msg)
  except:
    msg = {'msg' : 'stockfish load error plz try later'}
    return JsonResponse(msg)

class Pgn(Schema):
  pgn:str

@api.post('pgntouci')
def pgn_to_uci(request, pgn:Pgn):
  try:
    stockfish = get_stock_fish()

    data = pgn.pgn.split(' ')
    for i in range(len(data)):
      if data[i].endswith('.'):
        data[i] = None
      
      if i == len(data)-1:
        if data[i].find('-'):
          data[i] = None
    data = list(filter(None,data))
    board = chess.Board()
    uci = []
    for san in data:
      current = board.push_san(san).uci()
      stockfish.make_moves_from_current_position([current])
      uci.append(current)

    return ','.join(uci)
  except ValueError:
    msg = {'msg': 'unvalid move'}
    return JsonResponse(msg)

  except:
    msg = {'msg' : 'stockfish load error plz try later'}
    return JsonResponse(msg)

class Uci(Schema):
  uci:str


@api.post('/evaluate')
def evaluate(request, uci:Uci):
  try:
    res = []
    stockfish = get_stock_fish()
    stockfish.set_position()
    color = ['W', 'B']
    cnt = 0

    for i in uci.uci.split(','):
      if not stockfish.is_move_correct(i):
        return JsonResponse({'msg' : 'unvaild move is detected'})
    
      best_move = stockfish.get_top_moves(1)[0]
      stockfish.make_moves_from_current_position([i])

      eval = stockfish.get_evaluation()

      if best_move['Centipawn'] < 0 and eval['value'] < 0:
        msg = eval_position(abs(best_move['Centipawn'] - eval['value']))
      elif best_move['Centipawn'] < 0 or eval['value'] < 0:
        msg = eval_position(abs(best_move['Centipawn']) + abs(eval['value']))
      else:
        msg = eval_position(abs(best_move['Centipawn'] - eval['value']))
        

      res.append({'color' : color[cnt%2], 'move' : i, 'best' : best_move, 'eval' : eval, 'msg' : msg})

      cnt += 1

    return JsonResponse(res, safe=False)
  except:
    return JsonResponse({'msg' : 'evaluation fali'})

urlpatterns = [
    path('api/', api.urls),
]
