from django.test import TestCase, Client
from django.urls import reverse
from leads.forms import ContactForm
from django.contrib import messages


class HomePageViewTest(TestCase):

    def test_home_page_view(self):
        # Test if the home page returns a 200 status code
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class ContactUsPageViewTest(TestCase):

    def test_contact_us_page_view_GET(self):
        # Test if the contact us page returns a 200 status code for GET request
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_us_page_view_POST_valid_form(self):
        # Test if the contact us page redirects to the home page for a valid POST request
        form_data = {'name': 'John Doe', 'email': 'john@example.com', 'message': 'Hello, this is a test message.'}
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertRedirects(response, reverse('home'))

    def test_contact_us_page_view_POST_invalid_form(self):
        # Test if the contact us page returns a 200 status code for an invalid POST request
        form_data = {'name': '', 'email': 'invalid_email', 'message': ''}
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 200)


class AboutUsPageViewTest(TestCase):

    def test_about_us_page_view(self):
        # Test if the about us page returns a 200 status code
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)


class PrivacyPageViewTest(TestCase):

    def test_privacy_page_view(self):
        # Test if the privacy page returns a 200 status code
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)


class FAQsPageViewTest(TestCase):

    def test_faqs_page_view(self):
        # Test if the FAQs page returns a 200 status code
        response = self.client.get(reverse('faqs'))
        self.assertEqual(response.status_code, 200)
