from django.shortcuts import render
from processor.chess_pipe.data_processor import DataProcessor
from chessdata.models import Opening

# Create your views here.
def main(request):
  Opening.objects.all().delete()
  DataProcessor()
  return render(request, "index.html")