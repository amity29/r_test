# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Flight(models.Model):
    id = models.AutoField(primary_key=True, blank = False)
    key = models.CharField(max_length = 250, blank = True)
    dataval =   models.TextField(blank = True)
    val = models.CharField(max_length = 20, blank = True)
    decision = models.CharField(max_length = 45, blank = True)
    ts = models.CharField(max_length = 45, blank = True)
    date = models.CharField(max_length = 250, blank = True)
    sc = models.CharField(max_length = 250, blank = True)
    dest = models.CharField(max_length = 45, blank = True)
    depart  = models.CharField(max_length = 45, blank = True)
    arrival = models.CharField(max_length = 45, blank = True)
    airline  = models.CharField(max_length = 45, blank = True)
    price  = models.CharField(max_length = 45, blank = True)
    price_int   = models.CharField(max_length = 45, blank = True)
    win_decision = models.CharField(max_length = 45, blank = True)
    win_value  = models.CharField(max_length = 45, blank = True)
    current_winner = models.CharField(max_length = 100, blank = True)
    comp   = models.CharField(max_length = 5000, blank = True)
    ts_recent  = models.DateTimeField(auto_now=True, blank = False)

    class Meta:
        db_table = 'flightscrapdata'
