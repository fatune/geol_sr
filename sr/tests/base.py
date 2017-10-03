from django.test import TestCase
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.models import Token

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

        self.assertTrue(fact.create_cards())
        self.assertRaises(ValueError,fact.create_cards)

        fact2 = subject.fact_set.create(order=10)

        fact2.field1 = "A fact 10"
        fact2.field2 = "Explaination of a fact 10"
        fact2.save()

        self.assertTrue(fact2.create_cards())
        self.assertRaises(ValueError,fact2.create_cards)

        self.assertEqual(Fact.objects.all().count(), 2)

        self.assertEqual(Card.objects.all().count(), 4)

        self.user = User(email='a@b.com')
        self.user2 = User(email='a2@b.com')

        token = Token.objects.create(email='a@b.com')

        #login = self.client.login(username='testuser', password='12345')
        login = self.client.login(uid=token.uid)
        self.assertTrue(login)

        subject2 = Subject.objects.create()
        subject2.title = 'Title2'
        subject2.save()

        # setup facts with pictures
        subject3 = Subject.objects.create()
        subject3.title = 'Subj with pictures'
        subject3.save()

