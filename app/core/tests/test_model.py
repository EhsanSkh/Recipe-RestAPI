from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="ehsanadmin@gmail.com", password="some-password"):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email(self):
        email = "ehsanadmin@gmail.com"
        password = "sarisari"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        email = "ehsanadnin@gmAIL.cOM"
        user = get_user_model().objects.create_user(
            email=email,
            password="some-password"
        )
        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="some-password"
            )

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="ehsanadmin@gmail.com",
            password="some-password"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )
        self.assertEqual(str(tag), tag.name)
