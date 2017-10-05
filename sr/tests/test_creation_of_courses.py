from sr.models import Subject, Fact, Card, Memory, NoFactToLearn, NoCardToLearn

from .base import UTests

from sr.import_course import import_course_from_csv

class NewCourseCreationTest(UTests):

    def test_creating_new_subject(self):

        self.assertEquals(Subject.objects.filter(title='Cities').count(), 0)
        cards_before = Card.objects.all().count()

        import_course_from_csv('./courses/cities.csv', 'Cities')
        subjects = Subject.objects.filter(title='Cities')
        self.assertEqual(subjects.count(), 1)


        facts = Fact.objects.filter(subject=subjects[0])
        self.assertEquals(facts.count(), 2)

        card0 = Card.objects.filter(fact=facts[0])[0]
        card1 = Card.objects.filter(fact=facts[1])[0]

        self.assertEqual(card0.front_text, 'Russia' )
        self.assertEqual(card0.back_text, 'Moscow' )
        self.assertEqual(card1.front_text, 'Ukraine' )
        self.assertEqual(card1.back_text, 'Kiev' )

        self.assertEqual(Card.objects.all().count(), cards_before+4)


    def test_raises_error_when_subject_already_exists(self):
        import_course_from_csv('./courses/cities.csv', 'Cities')
        self.assertRaises(ValueError, import_course_from_csv, './courses/cities.csv', 'Cities')
