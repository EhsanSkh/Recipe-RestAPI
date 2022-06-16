from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipes.serializers import IngredientSerializer


INGREDIENTS_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ehsanadmin@gmail.com",
            password="some-password"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredientss(self):
        Ingredient.objects.create(name="test-name-1", user=self.user)
        Ingredient.objects.create(name="test-name-2", user=self.user)
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            email="user2@gmail.com",
            password="some-password"
        )
        Ingredient.objects.create(name="name-user-2", user=user2)
        ingredients = Ingredient.objects.create(name="name-user-1", user=self.user)
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredients.name)

    def test_create_ingredients(self):
        payload = {"name": "some-name"}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        payload = {"name": ""}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
