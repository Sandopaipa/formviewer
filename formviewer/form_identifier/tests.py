from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse


class TestValidateFormView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get_form')

    def test_validate_date1(self):
        data = "field1=01.01.2001"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_validate_date2(self):
        data = "field1=2001-01-01"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_validate_text(self):
        data = "field1=text"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_validate_phone(self):
        data = "field1=+7 000 000 00 00"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_validate_email(self):
        data = "field1=usermail@mail.mail"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_wrong_fieldset1(self):

        data = "field1=text&FORM1=01.01.2001"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 203)

    def test_wrong_fieldset2(self):
        data = "field1=text&field2=text"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 203)
