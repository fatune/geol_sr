from django.test import TestCase
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.models import Token

from sr.models import Subject, Fact, Card, create_cards_simple

class UTests(TestCase):

    def setUp(self):
        subject = Subject.objects.create()
        subject.title = 'My Title'
        subject.save()
        subject.fact_set.all()

        fact = subject.fact_set.create(order=1)
        fact.save()

        create_cards_simple(fact, 'A fact 1', 'A fact 1 back')
        self.assertRaises(ValueError,create_cards_simple, fact, 'A fact 1', 'A fact 1 back')

        fact2 = subject.fact_set.create(order=10)
        fact2.save()

        create_cards_simple(fact2, 'A fact 10', 'A fact 10 back')
        self.assertRaises(ValueError,create_cards_simple, fact2, 'A fact 10', 'A fact 10 back')

        self.assertEqual(Fact.objects.all().count(), 2)
        self.assertEqual(Card.objects.all().count(), 4)

        self.user = User(email='a@b.com')
        self.user2 = User(email='a2@b.com')

        token = Token.objects.create(email='a@b.com')

        login = self.client.login(uid=token.uid)
        self.assertTrue(login)

        subject2 = Subject.objects.create()
        subject2.title = 'Title2'
        subject2.save()
