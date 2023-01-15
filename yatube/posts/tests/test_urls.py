from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        """Smoke test."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='kataliz')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def test_urls_uses_correct_template(self):
        """Проверка страниц, доступных всем пользователям"""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.user}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.pk}
                    ): 'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_correct_template(self):
        """Проверка страницы редактирования поста (только автор)"""
        response = self.guest_client.get(reverse('posts:post_edit',
                                         kwargs={'post_id': self.post.pk})
                                         )
        auth_response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(auth_response.status_code, HTTPStatus.OK)

    def test_post_create_correct_template(self):
        """Проверка страницы создания поста (авторизованный)"""
        response = self.guest_client.get(reverse('posts:post_create'),
                                         follow=True
                                         )
        auth_response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')
        self.assertEqual(auth_response.status_code, HTTPStatus.OK)

    def test_404_error(self):
        """Проверка несуществующей страницы"""
        response = self.guest_client.get('blabla_page')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
