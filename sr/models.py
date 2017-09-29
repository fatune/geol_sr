from django.db import models

class Subject(models.Model):
    title = models.TextField(default='')

class Fact(models.Model):
    subject = models.ForeignKey(to=Subject)
    field1 = models.TextField(default='')
    field2 = models.TextField(default='')

    def create_cards(self):
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
