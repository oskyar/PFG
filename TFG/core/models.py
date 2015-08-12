from django.db import models
from django.contrib import admin
# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

#Asignatura
class Subject(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
#FK Tema

#Tema
class Topic(models.Model):
    cardinality = models.IntegerField
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

admin.site.register(Subject )
admin.site.register(Topic )
