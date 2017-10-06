from tempfile import NamedTemporaryFile


from .base import UTests
from sr.models import Subject, Fact, Card, Memory, NoFactToLearn, NoCardToLearn
from sr.import_course import (import_course_from_csv,
                              import_course_from_csv_similar_second_card,
                              import_cards_from_csv)

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

    def test_loading_temp_csv_file(self):
        lines = [b' Field1; Field2 ; Field 3  ;Hello world!\n',
                 b'Rfield1; Rfield2;   Rfield4  ;   Second line  ']
        lines_splited = [l.decode('utf-8').split(';') for l in lines]

        with NamedTemporaryFile() as tf:
            tf.writelines(lines)
            tf.seek(0)
            cards = import_cards_from_csv(tf.name)
            self.assertEqual(len(cards), 2,
                'Number of lines in file must match number of readed facts')
            line1 = [lines_splited[0][i].strip() == cards[0][i] for i in range(2)]
            self.assertTrue(all(line1), 'All Fields must be with removed leading and trailing spaces')


    def test_raises_error_when_subject_already_exists(self):
        import_course_from_csv('./courses/cities.csv', 'Cities')
        self.assertRaises(ValueError, import_course_from_csv, './courses/cities.csv', 'Cities')
        self.assertRaises(ValueError, import_course_from_csv_similar_second_card, './courses/cities.csv', 'Cities')
