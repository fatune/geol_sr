from sr.models import Subject, Fact, Card, Memory

from .base import UTests

class ListAndItemModelsTest(UTests):

    def test_getting_item(self):

        subjects = Subject.objects.all()

        self.assertTrue(subjects.count()==2)
        self.assertTrue(any(s.title =='My Title' for s in subjects))

        subject = subjects[0]

        facts = Fact.objects.all()
        self.assertTrue(facts.count()>0)
        self.assertTrue(any(f.field1 =='A fact 1' for f in facts))
        self.assertTrue(any(f.field2 =='Explaination of a fact 1' for f in facts))

        fact = facts[0]
        cards = Card.objects.filter(fact=fact)
        self.assertTrue(cards.count()==2)

        self.assertEqual(cards[0].front,'A fact 1')
        self.assertEqual(cards[0].back,'Explaination of a fact 1')
        self.assertEqual(cards[1].back,'A fact 1')
        self.assertEqual(cards[1].front,'Explaination of a fact 1')

        subject.refresh_from_db()


    def test_gettin_next_card(self):
        subject = Subject.objects.filter(title='My Title')[0]

        next_card = subject.get_next_card(self.user)

        self.assertTrue(next_card)
        self.assertTrue(next_card.format_card()['front']=='A fact 1')
        self.assertTrue(next_card.format_card()['back']=='Explaination of a fact 1')

        next_card = subject.get_next_card(self.user)
        self.assertTrue(next_card)
        self.assertTrue(next_card.format_card()['front']=='A fact 1')
        self.assertTrue(next_card.format_card()['back']=='Explaination of a fact 1')

        subject = Subject.objects.filter(title='Title2')[0]

        self.assertRaises(ValueError,subject.get_next_card,self.user)

        #next_card = subject.get_next_card(self.user)

        #self.assertTrue(next_card)
        #self.assertTrue(next_card.format_card()['front']=='A fact 1')
        #self.assertTrue(next_card.format_card()['back']=='Explaination of a fact 1')

        #next_card = subject.get_next_card(self.user)
        #self.assertTrue(next_card)
        #self.assertTrue(next_card.format_card()['front']=='A fact 1')
        #self.assertTrue(next_card.format_card()['back']=='Explaination of a fact 1')

