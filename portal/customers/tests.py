from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Customer


class CustomerViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pw12345!')
        self.customer = Customer.objects.create(name='Acme AS')

    def test_list_requires_login(self):
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_view_customer(self):
        self.client.login(username='alice', password='pw12345!')
        response = self.client.get(reverse('customer_detail', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acme AS')
