from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Menu, Item, Ingredient
from .forms import MenuForm

import datetime


class MenuTest(TestCase):
    client = Client()

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testguy',
            email = 'testguy@test.com',
            password = 'testguy'
        )

        self.ingredient_1 = Ingredient.objects.create(name='cheese')
        self.ingredient_2 = Ingredient.objects.create(name='onions')

        self.item_1 = Item.objects.create(
            name="Cheesy Onions",
            description="Its so good to eat",
            standard = True,
            chef = self.user
        )

        self.item_2 = Item.objects.create(
            name="Sandwich",
            description="Bread is toasted but not really",
            standard=False,
            chef = self.user
        )

        self.item_1.ingredients.add(self.ingredient_1)
        self.item_2.ingredients.set([self.ingredient_1, self.ingredient_2])

        self.menu_1 = Menu.objects.create(
            season='Summer',
            expiration_date=datetime.date.today(),
        )

        self.menu_2 = Menu.objects.create(
            season='Winter',
            expiration_date=datetime.date.today() + datetime.timedelta(days=5),
        )

        self.menu_1.items.add(self.item_1)
        self.menu_2.items.set([self.item_1, self.item_2])

    def test_menu_list(self):
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu:menu_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_menu_new(self):
        data = {
            'season': 'Winter',
            'items': [self.item_1.id, self.item_2.id],
            'expiration': '12/25/2018',
        }
        resp = self.client.post('/menu/new/', data)
        resp_2 = self.client.get(reverse('menu:menu_new'))
        self.assertEqual(resp_2.status_code, 200)
        self.assertEqual(resp.status_code, 200)

    def test_menu_form(self):
        form = MenuForm(data={'season': 'Winter',
                              'items': [self.item_1.id, self.item_2.id],
                              'expiration_date': '12/25/2018',
                              'created_date': datetime.date.today()})
        self.assertTrue(form.is_valid())

    def test_menu_form_fail(self):
        form = MenuForm(data={})
        self.assertFalse(form.is_valid())

    def test_menu_edit(self):
        data = {
            'season': 'Winter',
            'items': [self.item_1.id, self.item_2.id],
            'expiration': '12/25/2018',
        }
        resp_1 = self.client.post(reverse('menu:menu_edit', kwargs={'pk': 1}), data)
        resp_2 = self.client.get(reverse('menu:menu_edit', kwargs={'pk': 1}))
        self.assertEqual(resp_1.status_code, 200)
        self.assertEqual(resp_2.status_code, 200)


class ItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testguy',
            email='testguy@test.com',
            password='testguy'
        )

        self.item_1 = Item.objects.create(
            name="Cheesy Onions",
            description="Its so good to eat",
            standard=True,
            chef=self.user
        )
        self.ingredient_1 = Ingredient.objects.create(name='cheese')
        self.ingredient_2 = Ingredient.objects.create(name='onions')

    def test_item_list(self):
        resp = self.client.get(reverse('menu:item_list'))
        self.assertEqual(resp.status_code, 200)

    def test_item_detail(self):
        resp = self.client.get(reverse('menu:item_detail', kwargs={'pk': self.item_1.id}))
        self.assertEqual(resp.status_code, 200)

