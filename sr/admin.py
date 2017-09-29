from django.contrib import admin

from .models import Subject, Fact, Card

admin.site.register(Subject)
admin.site.register(Fact)
admin.site.register(Card)
