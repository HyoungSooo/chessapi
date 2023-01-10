from django.test import TestCase, Client
import json
import unittest
from api.models import *
import pandas as pd
from api.apiutils import get_stock_fish
from django.http import JsonResponse


class EvaluationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.c = Client()
        self.stockfish = get_stock_fish()

    def test_pgn_to_uci(self):
      data = "1. d4 e5 2. dxe5 d6 3. f4 Bg4 4. Nf3 Nc6 5. Nc3 dxe5 6. Nxe5 Nxe5 7. fxe5 Qxd1+ 8. Nxd1 Bf5 9. Ne3 Be4 10. Bd2 O-O-O 11. O-O-O Nh6 12. Bc3 Bc5 13. Nc4 Rxd1+ 14. Kxd1 Ng4 15. Rg1 Rd8+ 16. Kc1 Bxg1 17. h3 Nh2 18. Ne3 0-1"
      res = self.c.post('http://127.0.0.1:8000/api/pgntouci',data = {'pgn': data} , content_type= 'application/json')

      self.assertEqual(res.status_code, 200)
      
      content = json.loads(res.content)

      try:
        for i in content.split(','):
          self.stockfish.make_moves_from_current_position([i])
      except:
        self.assertTrue(False, "this uci is unvaild")

    
    def test_unvaild_pgn_detect(self):

      data = "1. d4 d4 0-1"
      res = self.c.post('http://127.0.0.1:8000/api/pgntouci',data = {'pgn': data} , content_type= 'application/json')
      self.assertEqual(res.status_code, 200)
      content = json.loads(res.content)

      self.assertEqual('unvalid move', content['msg'])

    def test_evaluate_user_uci(self):
      data = "1. d4 e5 2. dxe5 d6 3. f4 Bg4 4. Nf3 Nc6 5. Nc3 dxe5 6. Nxe5 Nxe5 7. fxe5 Qxd1+ 8. Nxd1 Bf5 9. Ne3 Be4 10. Bd2 O-O-O 11. O-O-O Nh6 12. Bc3 Bc5 13. Nc4 Rxd1+ 14. Kxd1 Ng4 15. Rg1 Rd8+ 16. Kc1 Bxg1 17. h3 Nh2 18. Ne3 0-1"
      uci = self.c.post('http://127.0.0.1:8000/api/pgntouci',data = {'pgn': data} , content_type= 'application/json')

      uci = json.loads(uci.content)

      res = self.c.post('http://127.0.0.1:8000/api/evaluate', data = {'uci': uci}, content_type= 'application/json')

      self.assertEqual(res.status_code, 200)

      data:dict = json.loads(res.content)

      self.assertEqual(len(uci.split(',')), len(data))

      for key in data:
        self.assertIn('eval', key)
        self.assertIn('best', key)
        self.assertIn('color', key)




      