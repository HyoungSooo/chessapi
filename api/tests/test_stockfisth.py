from stockfish import Stockfish
from django.test import TestCase, Client
from django.urls import resolve, reverse
import json
import unittest
from api.models import *
from api.apiutils import find_latest_file, get_stock_fish
import pandas as pd





class StockFishTest(unittest.TestCase):
  def setUp(self) -> None:
    self.c = Client()
    self.stockfish = get_stock_fish()

  
  def test_stockfish_is_work(self):
    self.assertTrue(self.stockfish.get_fen_position())

  def test_stockfish_api_give_best_moves(self):
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    res = self.c.get(f'http://127.0.0.1:8000/api/stockfish?fen={fen}')

    self.assertEqual(res.status_code, 200)

    data = json.loads(res.content)

    for i in data:
      self.assertEqual(len(i), 3)

      self.assertTrue(i['Move'])
      try:
        self.assertTrue(i['Centipawn'])
      except:
        self.assertEqual(i['Centipawn'], None)

      try:
        self.assertTrue(i['Mate'])
      except:
        self.assertEqual(i['Mate'], None)

