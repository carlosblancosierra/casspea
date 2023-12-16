# store/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from boxes.models import BoxSize


class StoreHomePageViewTest(TestCase):
    def test_home_page_view(self):
        # Test if the home page returns a 200 status code
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)


class BoxPageViewTest(TestCase):

    def test_box_page_view(self):
        response = self.client.get(reverse('store:boxes', args=['box-24']))
        print(response.content.decode())
        self.assertEqual(response.status_code, 200)
