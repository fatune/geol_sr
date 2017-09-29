from django.db import models

class Subject(models.Model):
    title = models.TextField(default='')

class Fact(models.Model):
    subject = models.ForeignKey(to=Subject)
    field1 = models.TextField(default='')
    field2 = models.TextField(default='')
