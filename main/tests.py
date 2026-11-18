from django.test import TestCase


class HealthzTest(TestCase):
    def test_healthz_ok(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)