from django.test import TestCase, Client
import json
import unittest
from api.models import *
import pandas as pd
from api.apiutils import get_stock_fish


class StockFishTest(unittest.TestCase):
  def setUp(self) -> None:
    self.c = Client()
    self.stockfish = get_stock_fish()
  
  def test_create_fen_by_moves(self):

    res = self.c.get('http://127.0.0.1:8000/api/getfen?move=e2e4,e7e5,d2d4,e5d4,d1d4')

    self.assertEqual(res.status_code, 200)

    data = json.loads(res.content)
    self.assertTrue(self.stockfish.is_fen_valid(data['fen']))

  def test_return_error_when_get_uvaild_move(self):

    res = self.c.get('http://127.0.0.1:8000/api/getfen?move=e2e4,e4e5')

    self.assertEqual(res.status_code, 200)

    data = json.loads(res.content)

    self.assertEqual(data['msg'], 'unvalid move')
    

    
