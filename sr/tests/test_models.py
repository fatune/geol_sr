from freezegun import freeze_time
import pytz

from django.utils import timezone

from sr.models import Subject, Fact, Card, Memory

from .base import UTests

from unittest import skip



class ListAndItemModelsTest(UTests):

    def test_getting_item(self):

        subjects = Subject.objects.all()

        self.assertTrue(subjects.count()==2)
        self.assertTrue(any(s.title =='My Title' for s in subjects))

        subject = subjects[0]

        facts = Fact.objects.all()
        self.assertTrue(facts.count()==2)
        self.assertTrue(any(f.field1 =='A fact 1' for f in facts))
        self.assertTrue(any(f.field2 =='Explaination of a fact 1' for f in facts))

        self.assertTrue(any(f.field1 =='A fact 10' for f in facts))
        self.assertTrue(any(f.field2 =='Explaination of a fact 10' for f in facts))

        fact = facts[0]
        fact2= facts[1]

        self.assertEqual(fact2.field1, "A fact 10")

        cards = Card.objects.filter(fact=fact)
        cards2 = Card.objects.filter(fact=fact2)

        self.assertEqual(Card.objects.all().count(), 4)

        self.assertEqual(cards[0].front,'A fact 1')
        self.assertEqual(cards[0].back,'Explaination of a fact 1')
        self.assertEqual(cards[1].front,'Explaination of a fact 1')
        self.assertEqual(cards[1].back,'A fact 1')

        self.assertEqual(cards2[0].front,'A fact 10')
        self.assertEqual(cards2[0].back,'Explaination of a fact 10')
        self.assertEqual(cards2[1].front,'Explaination of a fact 10')
        self.assertEqual(cards2[1].back,'A fact 10')

    def test_gettin_next_card(self):
        subject = Subject.objects.filter(title='My Title')[0]

        next_memory_object = subject.get_next_card(self.user)

        self.assertTrue(next_memory_object)
        self.assertTrue(next_memory_object.format_card()['front']=='A fact 1')
        self.assertTrue(next_memory_object.format_card()['back']=='Explaination of a fact 1')

        next_memory_object = subject.get_next_card(self.user)
        self.assertTrue(next_memory_object)
        self.assertTrue(next_memory_object.format_card()['front']=='A fact 1')
        self.assertTrue(next_memory_object.format_card()['back']=='Explaination of a fact 1')

        subject = Subject.objects.filter(title='Title2')[0]

        self.assertRaises(ValueError,subject.get_next_card,self.user)

    def test_rate_card(self):
        subject = Subject.objects.filter(title='My Title')[0]

        with freeze_time('2000-01-01 00:00:00'):
            self.assertEqual( timezone.datetime.now(),timezone.datetime(2000, 1, 1))
            next_memory_object = subject.get_next_card(self.user)
            self.assertEqual( next_memory_object.to_be_answered, timezone.datetime.now(pytz.utc))
            self.assertTrue(next_memory_object.rate(-1))

        with freeze_time('2000-01-01 00:00:10'):
            self.assertEqual( next_memory_object.to_be_answered, timezone.datetime.now(pytz.utc))
            self.assertTrue(next_memory_object.rate(0))

        with freeze_time('2000-01-01 00:00:40'):
            self.assertEqual( next_memory_object.to_be_answered, timezone.datetime.now(pytz.utc))
            self.assertTrue(next_memory_object.rate(1))

        with freeze_time('2000-01-01 00:01:40'):
            self.assertEqual( next_memory_object.to_be_answered, timezone.datetime.now(pytz.utc))

    def test_get_next_card_after_rate_first(self):

        subject = Subject.objects.filter(title='My Title')[0]
        self.assertEqual(Memory.objects.filter(subject=subject, user = self.user).count(), 0)

        next_memory_object = subject.get_next_card(self.user)
        self.assertEqual(Memory.objects.filter(subject=subject, user = self.user).count(), 2)
        self.assertEqual(next_memory_object.format_card()['front'], 'A fact 1')
        next_memory_object.rate(1)

        next_memory_object = subject.get_next_card(self.user)
        self.assertEqual(Memory.objects.filter(subject=subject, user = self.user).count(), 4)
        self.assertEqual(next_memory_object.format_card()['front'], 'A fact 10')
        next_memory_object.rate(1)

        self.assertRaises(ValueError,subject.get_next_card,self.user)

        next_memory_object = subject.get_next_card(self.user2)
        self.assertEqual(Memory.objects.filter(subject=subject, user = self.user2).count(), 2)
        self.assertEqual(next_memory_object.format_card()['front'], 'A fact 1')
        next_memory_object.rate(1)
