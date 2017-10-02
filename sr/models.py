from django.db import models
from django.db.models import Q

#from django.contrib.auth.models import User
from accounts.models import SrUser as User

from django.utils import timezone

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
            to_be_repeated = Memory.objects.filter(user=user, subject=self,
                             to_be_answered__lt = timezone.now() + timezone.timedelta(seconds=1))

            if to_be_repeated.count() == 0:
                try:
                    self.add_new_card_to_memories(user)
                    continue
                except NoFactToLearn:
                    if to_be_repeated.count() < Memory.objects.filter(user=user, subject=self).count():
                        raise NoCardToLearn ("There is no cards to learn yet")
                    else:
                        raise NoFactToLearn ("There is no new fact to learn")

            memory = to_be_repeated[0]
            break

        return memory

    def add_new_card_to_memories(self, user):
        facts = Fact.objects.filter(subject=self).order_by('order')
        memories = Memory.objects.filter(user=user, subject=self).order_by('-fact__order')

        if memories.count() == 0:
            # if there is no memoriesed facts yet, take cards of first fact
            # if there is no facts at all raise error
            if facts.count()>0:
                new_fact = facts[0]
            else:
                raise NoFactToLearn ("There is no new fact to learn")
        else:
            # if there is memoriesed facts, check order of last memorised and take this and next fact
            # if there is no new facts at all raise error
            last_memorised_fact_order = memories[0].fact.order
            new_facts = facts.filter(order__gt = last_memorised_fact_order)
            if new_facts.count() >0:
                new_fact = new_facts[0]
            else:
                raise NoFactToLearn ("There is no new fact to learn")

        cards = Card.objects.filter(fact=new_fact)
        for i,card in enumerate(cards):
            m = card.memory_set.create(user = user,
                                       fact = new_fact,
                                       subject = self,)

            m.to_be_answered = timezone.now() + timezone.timedelta(seconds=i*60)# - timezone.timedelta(seconds=5)
            m.save()


class Fact(models.Model):
    subject = models.ForeignKey(to=Subject)
    field1 = models.TextField(default='')
    field2 = models.TextField(default='')
    order = models.IntegerField(unique=True)


    def create_cards(self):
        # check if there is no cards about this fact yet
        cards = Card.objects.filter(fact=self)
        if cards.count() > 0: raise ValueError ("There are cards about this fact already")

        card_front = self.card_set.create()
        card_front.front = self.field1
        card_front.back = self.field2
        card_front.save()

        card_back = self.card_set.create()
        card_back.front = self.field2
        card_back.back = self.field1
        card_back.save()

        return True


class Card(models.Model):
    fact = models.ForeignKey(to=Fact)
    front = models.TextField(default='')
    back = models.TextField(default='')

class Memory(models.Model):
    memory_strength = models.FloatField(default=0)
    last_answered = models.DateTimeField(auto_now_add=True)
    to_be_answered = models.DateTimeField(null=True, default=None, blank=True)
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    fact = models.ForeignKey(Fact)
    subject = models.ForeignKey(Subject)

    def format_card(self):
        return {'front' : self.card.front,
                'back' : self.card.back}

    def rate(self, score):
        if score < 0:
            self.memory_strength = 0
            delta = timezone.timedelta(seconds=10)
        else:
            self.memory_strength += score
            if self.memory_strength < 1: delta = timezone.timedelta(seconds=30)
            elif self.memory_strength < 2: delta = timezone.timedelta(seconds=60)
            elif self.memory_strength < 3: delta = timezone.timedelta(seconds=300)
            elif self.memory_strength < 4: delta = timezone.timedelta(seconds=3600*12)
            elif self.memory_strength >= 4: delta = timezone.timedelta(days=2**(self.memory_strength-4))
        self.last_answered = timezone.now()
        self.to_be_answered = timezone.now() + delta
        self.save()
        return True

