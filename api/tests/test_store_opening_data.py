from django.test import TestCase, Client
from django.urls import resolve, reverse
import json
import unittest
from api.models import *
from api.apiutils import find_latest_file
import pandas as pd


class DataStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.c = Client()

    def test_upload_file_api_is_available(self):

        uploaded_file = open('api\\tests\\test.txt', 'rb')
        
        res = self.c.post('http://127.0.0.1:8000/api/opening', {'uploaded_file':uploaded_file})

        self.assertEqual(res.status_code, 200)
        
        with open('api\\tests\\test.txt') as fp:
            file1_contents = fp.read()

        with open('api\\dist\\data\\test.txt') as fp:
            file2_contents = fp.read()

        self.assertEqual(len(file1_contents), len(file2_contents))
    
    def test_uploaded_file_store_in_database(self):
        uploaded_file = open('api\\tests\\data.csv', 'rb')
        
        self.c.post('http://127.0.0.1:8000/api/opening', {'uploaded_file':uploaded_file})
        res = self.c.get('http://127.0.0.1:8000/api/opening/to_data?filename=data.csv')

        self.assertEqual(res.status_code, 200)

        with open('api\\tests\\data.csv') as fp:
            file1_contents = fp.read()

        with open('api\\dist\\data\\data.csv') as fp:
            file2_contents = fp.read()

        self.assertEqual(len(file1_contents), len(file2_contents))

        obj = ChessOpening.objects.all()
        data = pd.read_csv('api\\tests\\data.csv')

        self.assertEqual(len(obj), len(data))


        for i in data.index:
          if data.loc[i,'Move'] == 'start':
            self.assertEqual(data.loc[i,'Move'], obj[i].move)
          else:
            self.assertEqual(','.join(eval(data.loc[i,'Move'])), obj[i].move)
          self.assertEqual(str(data.loc[i,'Next Moves']), obj[i].next_move)
          self.assertEqual(data.loc[i,'Opening Name'], obj[i].name)

        


        

