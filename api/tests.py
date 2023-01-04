from django.test import TestCase

# Create your tests here.

from selenium import webdriver

browser = webdriver.Chrome('C:\\cromedriver\\chromedriver.exe')
browser.get('http://localhost:8000')


assert 'The install worked successfully! Congratulations!' in browser.title