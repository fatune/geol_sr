from sr.models import Subject, Fact, Card, Memory, NoFactToLearn, NoCardToLearn

from .base import UTests

from sr.import_course import import_course

class NewCourseCreationTest(UTests):

    def test_creating_new_subject(self):
        self.assertEquals(Subject.objects.filter(title='cities').count(), 0)
        import_course('sr/courses/cities.csv')
        subjects = Subject.objects.filter(title='cities')
        self.assertEqual(subjects.count(), 1)
        self.assertEquals(Fact.objects.filter(subject=subjects[0]), 2)

    def test_raises_error_when_subject_already_exists(self):
        import_course('sr/courses/cities.csv')
        self.assertRaises(ValueError, import_course, 'sr/courses/cities.csv')
