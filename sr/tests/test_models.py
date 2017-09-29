from django.test import TestCase
from django.db import models

from django.core.exceptions import ValidationError

from sr.models import Subject


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