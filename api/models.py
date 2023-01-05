from django.db import models

# Create your models here.

class ChessOpening(models.Model):
    move = models.TextField()
    next_move = models.TextField()
    name = models.TextField()
    wdl = models.CharField(max_length=100)