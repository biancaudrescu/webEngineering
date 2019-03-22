# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return " \"name\":{}, \"code\": {}".format(self.name, self.code)


class Carrier(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return " \"name\":{}, \"code\": {}".format(self.name, self.code)


class Time(models.Model):
    label = models.CharField(max_length=8,primary_key=True)
    year = models.IntegerField()
    month = models.IntegerField()


class Flights(models.Model):
    cancelled = models.IntegerField()
    on_time = models.IntegerField()
    total = models.IntegerField()
    delayed = models.IntegerField()
    diverted = models.IntegerField()

    def __str__(self):
        return " \"id\":{}, \"cancelled\": {},\"on_tme\": {},\"total\": {},\"delayed\": {},\"diverted\": {}".format(
            self.id, self.cancelled, self.on_time, self.total, self.delayed, self.diverted)


class NumDelays(models.Model):
    weather = models.IntegerField()
    security = models.IntegerField()
    late_aircraft = models.IntegerField()
    nat_avi_sys = models.IntegerField()
    carrier = models.IntegerField()

    def __str__(self):
        return " \"id\":{}, \"weather\": {},\"security\": {},\"late_aircraft\": {},\"nav_avi_sys\": {},\"carrier\": {}".format(
            self.id, self.weather, self.security, self.late_aircraft, self.nat_avi_sys, self.carrier)


class MinutesDelayed(models.Model):
    late_aircraft = models.IntegerField()
    weather = models.IntegerField()
    carrier = models.IntegerField()
    security = models.IntegerField()
    total = models.IntegerField()
    nat_avi_sys = models.IntegerField()

    def __str__(self):
        return " \"id\":{}, \"late_aircraft\": {},\"weather\": {},\"carrier\": {},\"security\": {},\"total\": {},\"nat_avi_sys\": {}".format(
            self.id, self.late_aircraft, self.weather, self.carrier, self.security, self.total, self.nat_avi_sys)


class Statistics(models.Model):
    num_del = models.OneToOneField(NumDelays, on_delete=models.CASCADE)
    minutes_del = models.OneToOneField(MinutesDelayed, on_delete=models.CASCADE)
    flights = models.OneToOneField(Flights, on_delete=models.CASCADE)


class StatisticsGroup(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    statistics = models.OneToOneField(Statistics, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)

    class meta:
        unique_together = ('airport', 'carrier', 'time')