from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Category
from django.test import Client


class CategoryMethodTests(TestCase):

    def setUp(self):  # Found that online don't know if there is a better way
        cat = Category.objects.create(name='Funny')

    def test_slug_line_creation(self):

             cat = Category.objects.get(name='Funny')
             self.assertEqual(cat.slug, 'funny')


class IndexViewTests(TestCase):

    def test_index_view_with_no_stories(self):

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no completed stories yet.")
        self.assertQuerysetEqual(response.context['completed_stories_top'], [])

    def test_index_view_with_no_ongoing_stories(self):

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no ongoing stories right now.")
        self.assertQuerysetEqual(response.context['ongoing_stories'], [])


class IndexCategoryTests(TestCase):

    def test_search_view_with_no_stories(self):

        c = Client()
        response = c.post('/accounts/login/', {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)