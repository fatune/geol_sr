from django.test import TestCase
from django.db import models

from django.core.exceptions import ValidationError

from sr.models import Subject, Fact, Card


class ListAndItemModelsTest(TestCase):

    def test_getting_item(self):
        subjects_ = Subject()
        subjects_.save()

        subject = Subject()
        subject.title = 'My Title'
        subject.save()

        subjects = Subject.objects.all()

        self.assertTrue(subjects.count()>0)

        self.assertTrue(any(s.title =='My Title' for s in subjects))

        subject.fact_set.all()

        fact = subject.fact_set.create()

        fact.field1 = "A fact 1"
        fact.field2 = "Explaination of a fact 1"
        fact.save()

        facts = Fact.objects.all()
        self.assertTrue(facts.count()>0)
        self.assertTrue(any(f.field1 =='A fact 1' for f in facts))
        self.assertTrue(any(f.field2 =='Explaination of a fact 1' for f in facts))

        self.assertTrue(fact.create_cards())

        cards = Card.objects.filter(fact=fact)
        self.assertTrue(cards.count()==2)

        self.assertEqual(cards[0].front,'A fact 1')
        self.assertEqual(cards[0].back,'Explaination of a fact 1')
        self.assertEqual(cards[1].back,'A fact 1')
        self.assertEqual(cards[1].front,'Explaination of a fact 1')
