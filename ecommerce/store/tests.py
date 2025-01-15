from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, Item, ItemProxy


class ItemViewTest(TestCase):
    def test_get_items(self):
    
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

    
        test_gif = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='test')
        item_1 = Item.objects.create(name='item_1', category=category, image=test_gif, slug='item_1')
        item_2 = Item.objects.create(name='item_2', category=category, image=test_gif, slug='item_2')

        response = self.client.get(reverse('store:items'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['items'].count(), 2)
        self.assertEqual(list(response.context['items']), [item_1, item_2])
        self.assertContains(response, item_1)
        self.assertContains(response, item_2)


class ItemDetailViewTest(TestCase):
    def test_get_item_by_slug(self):
        # Create an item
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        test_gif = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='Category 1')
        item = Item.objects.create(
            name='item_1', category=category, slug='item-1', image=test_gif)
        # Make a request to the Item detail view with the Item's slug
        response = self.client.get(
        reverse('store:item_detail', kwargs={'slug': 'item-1'}))

        # Check that the response is a success
        self.assertEqual(response.status_code, 200)

        # Check that the Item is in the response context
        self.assertEqual(response.context['item'], item)
        self.assertEqual(response.context['item'].slug, item.slug)


class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        test_gif = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.item = ItemProxy.objects.create(
            name='test_item', slug='test-item', category=self.category, image=test_gif)

    def test_status_code(self):
        response = self.client.get(
            reverse('store:category_list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('store:category_list', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'store/category_items.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('store:category_list', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['items'].first(), self.item)