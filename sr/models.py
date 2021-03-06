#from itertools import chain

from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.models import User

from .settings import *

class NoCardToLearn(Exception):
    def __init__(self, message):
        super().__init__(message)

class NoFactToLearn(Exception):
    def __init__(self, message=None):
        super().__init__(message)

class Subject(models.Model):
    title = models.TextField(default='')

    def get_next_card(self, user):
        while True:
            to_be_repeated = Memory.objects.filter(user=user,
                                                   card__fact__subject=self,
                                                   to_be_answered__lt = timezone.now() + \
                                                                        timezone.timedelta(seconds=1))

            if to_be_repeated.count() == 0:
                try:
                    self.add_new_card_to_memories(user)
                    continue
                except NoFactToLearn:
                    if to_be_repeated.count() < Memory.objects.filter(user=user, card__fact__subject=self).count():
                        raise NoCardToLearn ("There is no cards to learn yet")
                    else:
                        raise NoFactToLearn ("There is no new fact to learn")

            memory = to_be_repeated[0]
            break

        return memory

    def add_new_card_to_memories(self, user):
        facts = Fact.objects.filter(subject=self).order_by('order')
        memories_unsorted = Memory.objects.filter(user=user,
                                                  card__fact__subject=self)
        memories = sorted(memories_unsorted,
                          key=lambda m: m.card.fact.order,
                          reverse=True)

        if len(memories) == 0:
            # if there is no memoriesed facts yet, take cards of first fact
            # if there is no facts at all raise error
            if facts.count()>0:
                new_fact = facts[0]
            else:
                raise NoFactToLearn ("There is no new fact to learn")
        else:
            # if there is memoriesed facts, check order of last memorised and take this and next fact
            # if there is no new facts at all raise error
            last_memorised_fact_order = memories[0].card.fact.order
            new_facts = facts.filter(order__gt = last_memorised_fact_order)
            if new_facts.count() >0:
                new_fact = new_facts[0]
            else:
                raise NoFactToLearn ("There is no new fact to learn")

        cards = Card.objects.filter(fact=new_fact)
        for i,card in enumerate(cards):
            m = card.memory_set.create(user = user)
            m.to_be_answered = timezone.now() + timezone.timedelta(seconds=i*DELTA_POSTPONE.seconds)
            m.save()


class Fact(models.Model):
    subject = models.ForeignKey(to=Subject)
    explanation = models.TextField(default='')
    order = models.IntegerField()

def create_cards_simple(fact, front, back):
    # check if there is no cards about this fact yet
    cards = Card.objects.filter(fact=fact)
    if cards.count() > 0: raise ValueError ("There are cards about this fact already")

    f1 = fact.card_set.create()
    f1.front_text = front
    f1.back_text = back
    f1.save()

    f2 = fact.card_set.create()
    f2.front_text = back
    f2.back_text = front
    f2.save()

def create_cards_simple_with_similar_second_card(fact, front_text, front_img, back_text, back_img):
    # check if there is no cards about this fact yet
    cards = Card.objects.filter(fact=fact)
    if cards.count() > 0: raise ValueError ("There are cards about this fact already")

    f1 = fact.card_set.create()
    f1.front_text = "%s %s" % (front_text, front_img)
    f1.back_text = "%s %s " % (front_text, back_img)
    f1.save()

    f2 = fact.card_set.create()
    f2.front_text = "%s %s" % (back_text, back_img)
    f2.back_text = "%s %s" % (front_text, back_img)
    f2.save()


class Card(models.Model):
    fact = models.ForeignKey(to=Fact)
    front_text = models.TextField()
    back_text = models.TextField()

    def format_card(self):
        return {'front':self.front_text,
                'back':self.back_text}

def get_memorised_cards(user, subject):
    to_be_repeated = Memory.objects.filter(user=user,
                                           card__fact__subject=subject,
                                           to_be_answered__lt = timezone.now() + \
                                                                timezone.timedelta(seconds=3600)).order_by('to_be_answered')

    others = Memory.objects.filter(user=user,
                                   card__fact__subject=subject,
                                   to_be_answered__gt = timezone.now() ).order_by('card__fact__order')

    to_be = [m.card.fact.order for m in to_be_repeated]
    other = [m.card.fact.order for m in others]
    return to_be, other

class Memory(models.Model):
    card = models.ForeignKey(Card)
    user = models.ForeignKey(User)
    memory_strength = models.FloatField(default=0)
    last_answered = models.DateTimeField(auto_now_add=True)
    to_be_answered = models.DateTimeField(null=True, default=None, blank=True)

    def __str__(self):
        return self.card.front

    def rate(self, score):
        if score < 0:
            self.memory_strength = 0
            delta = DELTA_0
        else:
            self.memory_strength += score
            if self.memory_strength < 1: delta = DELTA_1
            elif self.memory_strength < 2: delta = DELTA_2
            elif self.memory_strength < 3: delta = DELTA_3
            elif self.memory_strength < 4: delta = DELTA_4
            elif self.memory_strength >= 4:
                delta = timezone.timedelta(days = DELTA_5.days**(self.memory_strength-4))
        self.last_answered = timezone.now()
        self.to_be_answered = timezone.now() + delta
        self.save()

        # postpone to_be_answered for all related cards
        memories = Memory.objects.filter(user=self.user,
                                         card__fact=self.card.fact,
                                        ).exclude(id__in=[self.id])
        for memory in memories:
            memory.to_be_answered = timezone.now() + DELTA_POSTPONE
            memory.save()

        return True

