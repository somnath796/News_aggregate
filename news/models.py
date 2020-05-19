from django.db import models

# Create your models here.

class Headline(models.Model):
	title = models.CharField(max_length=200,unique = True)
	image = models.URLField(null=True, blank=True,unique = True)
	url = models.TextField(unique = True)
	description = models.TextField(default='NULL')
	def __str__(self):
	    return self.title