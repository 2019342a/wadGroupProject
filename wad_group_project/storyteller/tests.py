from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Category, UserProfile, User, Story
from django.test import Client


class CategoryMethodTests(TestCase):  # Test for slug

    def test_slug_line_creation(self):

             cat = Category.objects.create(name='Funny')
             self.assertEqual(cat.slug, 'funny')


class UserMethodTests(TestCase):  # User test

    def test_age_creation(self):
        new_user = User.objects.create_user('theo')
        u = UserProfile.objects.create(age=10, user=new_user)
        self.assertEqual(u.age, 10)


class StoryMethodTests(TestCase):  # Story test

    def test_content_creation(self):
        new_user1 = User.objects.create_user('theo1')
        new_user2 = User.objects.create_user('theo2')
        u1 = UserProfile.objects.create(age=10, user=new_user1)
        u2 = UserProfile.objects.create(age=11, user=new_user2)
        cat = Category.objects.create(name='Funny')
        s = Story.objects.create(views=20, category=cat, title='Foo', creator='theo1',
                                 story_text='This is a test :).', rating=20, ending=True, ended=True)
        s.contributors.add(u1.user)
        s.save()
        s.contributors.add(u2.user)
        s.save()
        self.assertEqual(s.story_text, 'This is a test :).')


class IndexViewTests(TestCase):

    def test_index_view_with_no_stories(self):  # Index tests

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no completed stories yet.")
        self.assertQuerysetEqual(response.context['completed_stories_top'], [])

    def test_index_view_with_no_ongoing_stories(self):

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no ongoing stories right now.")
        self.assertQuerysetEqual(response.context['ongoing_stories'], [])


class LoginTests(TestCase):  # Login test

    def test_login(self):

        c = Client()
        response = c.post('/accounts/login/', {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)