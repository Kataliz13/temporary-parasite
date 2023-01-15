from django.conf import settings
from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        title_dict = {
            self.post.text[:settings.POST_LENGHT]: str(post),
            self.group.title: str(self.group),
        }
        for keys, values in title_dict.items():
            with self.subTest(keys=keys):
                self.assertEqual(keys, values)

    def test_title_label(self):
        """verbose_name поля title совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose = post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст поста')

    def test_title_help_text(self):
        """help_text поля title совпадает с ожидаемым."""
        post = PostModelTest.post
        help_text = post._meta.get_field('text').help_text
        print()
        self.assertEqual(help_text, 'Введите текст поста')
