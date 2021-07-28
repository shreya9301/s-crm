from django.test import TestCase
from django.shortcuts import reverse

class HomePageTest(TestCase):
    def  test_get(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landing_page.html")


