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