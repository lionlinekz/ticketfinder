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
	
class Car(models.Model):
	number = models.CharField(max_length=5)
	car_type = models.CharField(max_length=30)
	places = models.CharField(max_length=300)
	tariff = models.CharField(max_length=20)
	
class Ticket(models.Model):
	order_id = models.CharField(max_length=128)
	express_id = models.CharField(max_length=128)
	train = models.CharField(max_length=128)
	departure_date = models.CharField(max_length=10)
	departure_time = models.CharField(max_length=10)
	arrival_date = models.CharField(max_length=10)
	arrival_time = models.CharField(max_length=10)
	departure_station = models.CharField(max_length=50)
	arrival_station = models.CharField(max_length=50)
	car_number = models.CharField(max_length=3)
	car_type = models.CharField(max_length=20)
	seat_number = models.CharField(max_length=3)
	price = models.CharField(max_length=7)
	full_name = models.CharField(max_length=100)
