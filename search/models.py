from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Station(models.Model):
	code = models.CharField(max_length=128)
	short_name = models.CharField(max_length=128)
	long_name = models.CharField(max_length=128)
	city_kaz = models.CharField(max_length=128, blank=True, null=True)
	city_rus = models.CharField(max_length=128, blank=True, null=True)
	city_eng = models.CharField(max_length=128, blank=True, null=True)
	def __unicode__(self):
		return self.long_name
		
class TrainSeat(models.Model):
	number = models.CharField(max_length=128)
	direction = models.CharField(max_length=128)
	departure_time = models.CharField(max_length=128)
	arrival_time = models.CharField(max_length=128)
	duration = models.CharField(max_length=128)
	common_seats = models.CharField(max_length=128)
	common_tariff = models.CharField(max_length=128)
	sitting_seats = models.CharField(max_length=128)
	sitting_tariff = models.CharField(max_length=128)
	reserved_seats = models.CharField(max_length=128)
	reserved_tariff = models.CharField(max_length=128)
	compartment_seats = models.CharField(max_length=128)
	compartment_tariff = models.CharField(max_length=128)
	soft_seats = models.CharField(max_length=128)
	soft_tariff = models.CharField(max_length=128)
	luxury_seats = models.CharField(max_length=128)
	luxury_tariff = models.CharField(max_length=128)
