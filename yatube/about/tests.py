from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_static_pages(self):
        """Проверка статических страниц"""
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_404_error(self):
        """Проверка несуществующей страницы"""
        response = self.guest_client.get('blabla_page')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
