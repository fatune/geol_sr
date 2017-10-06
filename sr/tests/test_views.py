from freezegun import freeze_time
#from unittest import skip
from django.shortcuts import render_to_response

from sr.models import Subject, Fact, create_cards_simple

from .base import UTests

class HomePageTest(UTests):

    def test_always_rate_previous_card(self):
        with freeze_time('2000-01-01 00:00:00'):
            # see first question and send POST to see the answer
            response = self.client.get('/study/1/')
            self.assertIn('A fact 1', response.content.decode('utf-8'))
            self.assertNotIn('A fact 1 back', response.content.decode('utf-8'))

            response = self.client.post('/study/1/', data={'foo': '-1'})
            self.assertTemplateUsed(response, 'study.html' )

        with freeze_time('2000-01-01 00:00:05'):
            # see the first answer and rate it -1
            self.assertIn('A fact 1 back', response.content.decode('utf-8'))
            response = self.client.post('/study/1/', data={'rate': '-1'})

            self.assertRedirects(response, '/study/1/')

        with freeze_time('2000-01-01 00:00:06'):
            # see 2nd question and send POST to see the answer
            response = self.client.get('/study/1/')
            self.assertIn('A fact 10', response.content.decode('utf-8'))

            response = self.client.post('/study/1/', data={'foo': '-1'})
            self.assertTemplateUsed(response, 'study.html' )

        with freeze_time('2000-01-01 00:00:36'):
            # Wait 30 sec and still see the second answer
            response = self.client.get('/study/1/')
            self.assertIn('A fact 10', response.content.decode('utf-8'))



    def test_render_img_in_question(self):
        subject = Subject.objects.create(title='Subj with HTML')
        subject.save()

        fact = Fact.objects.create(subject=subject, order=1)
        fact.save()

        field1 = u'<img src="pic_mountain.jpg">'
        field2 = u'<img src="pic_mountain2.jpg">'
        create_cards_simple(fact, field1, field2)

        response = self.client.get('/study/%s/' % subject.id)
        self.assertTemplateUsed(response, 'study.html' )
        self.assertIn(field1, response.content.decode('utf-8'))

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_uses_study_templates(self):
        response = self.client.get('/study/1/')
        self.assertTemplateUsed(response, 'study.html' )

    def test_raises_error_when_wrong_subject_id_passed(self):
        response = self.client.get('/study/1346/')
        self.assertEqual(response.status_code, 404)

    def test_handles_no_fact_to_learn(self):
        response = self.client.get('/study/2/')
        self.assertTemplateUsed(response, 'no_fact_to_learn.html')

    def test_handles_no_card_to_learn(self):
        subject = Subject.objects.filter(title='My Title')[0]
        next_memory_object = subject.get_next_card(self.user)
        self.assertTrue(next_memory_object.rate(1))
        next_memory_object = subject.get_next_card(self.user)
        self.assertTrue(next_memory_object.rate(1))
        self.assertTrue(next_memory_object.rate(1))
        self.assertTrue(next_memory_object.rate(1))

        response = self.client.get('/study/1/')
        self.assertTemplateUsed(response, 'no_cards_to_learn.html')

    def test_anonymous_user_visits_study(self):
        self.client.logout()
        response = self.client.get('/study/1/')
        self.assertTemplateUsed(response, 'please_login.html')

    def test_user_visits_study_parent(self):
        response = self.client.get('/study/')
        self.assertTemplateUsed(response, 'study_list.html')

#class StudyViewTest(TestCase):
#
#    def study_uses_list_template(self):
#        list_ = List.objects.create()
#        response = self.client.get('/lists/%d/' % (list_.id,))
#        self.assertTemplateUsed(response, 'list.html')


#class NewListTest(TestCase):

  #  def test_can_save_a_POST_request(self):
  #      self.client.post('/lists/new', data={'item_text': 'A new list item'})

  #      self.assertEqual(Item.objects.count(), 1)
  #      new_item = Item.objects.first()
  #      self.assertEqual(new_item.text, 'A new list item')


  #  def test_redirects_after_POST(self):
  #      response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
  #      new_list = List.objects.first()
  #      self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

  #  def test_validation_errors_are_sent_back_to_home_page_template(self):
  #      response = self.client.post('/lists/new', data={'item_text': ''})
  #      self.assertEqual(response.status_code, 200)
  #      self.assertTemplateUsed(response, 'home.html')
  #      expected_error = escape("You can't have an empty list item")
  #      self.assertContains(response, expected_error)



#class NewItemTest(TestCase):
#
#    def test_can_save_a_POST_request_to_an_existing_list(self):
#        other_list = List.objects.create()
#        correct_list = List.objects.create()
#
#        self.client.post(
#            '/lists/%d/add_item' % (correct_list.id,),
#            data={'item_text': 'A new item for an existing list'}
#        )
#
#        self.assertEqual(Item.objects.count(), 1)
#        new_item = Item.objects.first()
#        self.assertEqual(new_item.text, 'A new item for an existing list')
#        self.assertEqual(new_item.list, correct_list)
#
#
#    def test_redirects_to_list_view(self):
#        other_list = List.objects.create()
#        correct_list = List.objects.create()
#
#        response = self.client.post(
#            '/lists/%d/add_item' % (correct_list.id,),
#            data={'item_text': 'A new item for an existing list'}
#        )
#
#        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
#
#
#
#class ListViewTest(TestCase):
#
#    def test_uses_list_template(self):
#        list_ = List.objects.create()
#        response = self.client.get('/lists/%d/' % (list_.id,))
#        self.assertTemplateUsed(response, 'list.html')
#
#
#    def test_passes_correct_list_to_template(self):
#        other_list = List.objects.create()
#        correct_list = List.objects.create()
#        response = self.client.get('/lists/%d/' % (correct_list.id,))
#        self.assertEqual(response.context['list'], correct_list)
#
#
#    def test_displays_only_items_for_that_list(self):
#        correct_list = List.objects.create()
#        Item.objects.create(text='itemey 1', list=correct_list)
#        Item.objects.create(text='itemey 2', list=correct_list)
#        other_list = List.objects.create()
#        Item.objects.create(text='other list item 1', list=other_list)
#        Item.objects.create(text='other list item 2', list=other_list)
#
#        response = self.client.get('/lists/%d/' % (correct_list.id,))
#
#        self.assertContains(response, 'itemey 1')
#        self.assertContains(response, 'itemey 2')
#        self.assertNotContains(response, 'other list item 1')
#        self.assertNotContains(response, 'other list item 2')
#
#
#
