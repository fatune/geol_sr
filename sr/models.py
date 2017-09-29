from django.db import models

class Subject(models.Model):
    title = models.TextField(default='')

