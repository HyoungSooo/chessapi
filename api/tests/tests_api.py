from django.test import TestCase, Client
from django.urls import resolve, reverse
import json
import unittest
# Create your tests here.

from selenium import webdriver

class ApiTest(unittest.TestCase):
  def setUp(self):
    self.c = Client()

  def tearDown(self) -> None:
    return 'test done'

  def test_get_opening_data_api_is_avaliable(self):
    response = self.c.get('http://127.0.0.1:8000/api/opening?move=start')

    self.assertEqual(response.status_code, 200)

  def test_opeing_api_data(self):
    move = 'e2e4'
    response = self.c.get(f'http://127.0.0.1:8000/api/opening?move={move}')

    self.assertEqual(response.status_code, 200, msg=f'{response.content}')
    data = json.loads(response.content)

    for value in data:
      self.assertEqual(len(value), 3, msg=f'{data}')

      self.assertTrue(value['move'])
      self.assertTrue(value['name'])
      self.assertTrue(value['wdl'])

      
    