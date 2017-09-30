from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from sr.models import Subject, Fact, Card

class UTests(TestCase):

    def setUp(self):
        subject = Subject.objects.create()
        subject.title = 'My Title'
        subject.save()

        subject.fact_set.all()

        fact = subject.fact_set.create(order=1)

        fact.field1 = "A fact 1"
        fact.field2 = "Explaination of a fact 1"
        fact.save()
        fact.full_clean()

        self.assertTrue(fact.create_cards())

        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        subject2 = Subject.objects.create()
        subject2.title = 'Title2'
        subject2.save()
