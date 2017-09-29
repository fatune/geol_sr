from django.test import TestCase
from django.db import models

from django.core.exceptions import ValidationError

from sr.models import Subject, Fact, Card

class UTests(TestCase):

    def setUp(self):
        subject = Subject.objects.create()
        subject.title = 'My Title'
        subject.save()

        subject.fact_set.all()

        fact = subject.fact_set.create()

        fact.field1 = "A fact 1"
        fact.field2 = "Explaination of a fact 1"
        fact.save()
        fact.full_clean()

        self.assertTrue(fact.create_cards())
