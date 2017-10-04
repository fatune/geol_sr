from freezegun import freeze_time
import pytz

from django.utils import timezone

from sr.models import Subject, Fact, Card, Memory, NoFactToLearn, NoCardToLearn

from .base import UTests

#from unittest import skip



class ListAndItemModelsTest(UTests):

    def test_basic_objects_hyerarchy(self):
        self.assertTrue(Subject.objects.all().count() > 1)
        subject = Subject.objects.filter(title='My Title')[0]

        facts = Fact.objects.filter(subject=subject)
        self.assertEqual(facts.count(), 2)
        self.assertEqual(facts[0].order, 1)
        self.assertEqual(facts[1].order, 10)

        cards = Card.objects.filter(fact__in = facts)
        self.assertEqual(cards.count(), 4)

        self.assertEqual(cards[0].front_text,'A fact 1')
        self.assertEqual(cards[1].back_text,'A fact 1')

        self.assertEqual(cards[2].front_text,'A fact 10')
        self.assertEqual(cards[3].back_text,'A fact 10')

        self.assertEqual(Memory.objects.all().count(), 0)


    def test_gettin_next_card(self):
        subject = Subject.objects.filter(title='My Title')[0]

        next_memory_object = subject.get_next_card(self.user)

        self.assertTrue(next_memory_object)
        self.assertTrue(next_memory_object.card.format_card()['front']=='A fact 1')
        self.assertTrue(next_memory_object.card.format_card()['back']=='A fact 1 back')

        next_memory_object = subject.get_next_card(self.user)
        self.assertTrue(next_memory_object)
        self.assertTrue(next_memory_object.card.format_card()['front']=='A fact 1')
        self.assertTrue(next_memory_object.card.format_card()['back']=='A fact 1 back')

        subject2 = Subject.objects.filter(title='Title2')[0]

        self.assertRaises(NoFactToLearn,subject2.get_next_card,self.user)

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
        self.assertEqual(Memory.objects.filter(card__fact__subject=subject, user = self.user).count(), 0)

        next_memory_object = subject.get_next_card(self.user)
        self.assertEqual(Memory.objects.filter(card__fact__subject=subject, user = self.user).count(), 2)
        self.assertEqual(next_memory_object.card.format_card()['front'], 'A fact 1')
        next_memory_object.rate(1)

        next_memory_object = subject.get_next_card(self.user)
        self.assertEqual(Memory.objects.filter(card__fact__subject=subject, user = self.user).count(), 4)
        self.assertEqual(next_memory_object.card.format_card()['front'], 'A fact 10')
        next_memory_object.rate(1)

        self.assertRaises(NoCardToLearn,subject.get_next_card,self.user)

        next_memory_object = subject.get_next_card(self.user2)
        self.assertEqual(Memory.objects.filter(card__fact__subject=subject, user = self.user2).count(), 2)
        self.assertEqual(next_memory_object.card.format_card()['front'], 'A fact 1')
        next_memory_object.rate(1)

    def test_always_return_the_same_card_if_not_rated(self):
        subject = Subject.objects.filter(title='My Title')[0]

        with freeze_time('2000-01-01 00:00:00'):
            next_memory_object = subject.get_next_card(self.user)

        with freeze_time('2000-01-01 00:01:00'):
            next_memory_object_ = subject.get_next_card(self.user)
            self.assertEqual(next_memory_object, next_memory_object_)

        with freeze_time('2000-01-01 01:01:00'):
            next_memory_object__ = subject.get_next_card(self.user)
            self.assertEqual(next_memory_object_, next_memory_object__)
