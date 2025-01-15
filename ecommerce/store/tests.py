from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, Item, ItemProxy


class BaseTest(TestCase):
    def setUp(self):
        # Create a reusable small GIF
        self.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.test_gif = SimpleUploadedFile(
            'test_image.gif', self.small_gif, content_type='image/gif'
        )


class ItemViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        # Create a category and items
        self.category = Category.objects.create(name='test')
        self.item_1 = Item.objects.create(
            name='item_1', category=self.category, image=self.test_gif, slug='item_1'
        )
        self.item_2 = Item.objects.create(
            name='item_2', category=self.category, image=self.test_gif, slug='item_2'
        )

    def test_get_items(self):
        response = self.client.get(reverse('store:items'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['items'].count(), 2)
        self.assertEqual(list(response.context['items']), [self.item_1, self.item_2])
        self.assertContains(response, self.item_1.name)
        self.assertContains(response, self.item_2.name)


class ItemDetailViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        # Create a category and an item
        self.category = Category.objects.create(name='Category 1')
        self.item = Item.objects.create(
            name='item_1', category=self.category, slug='item-1', image=self.test_gif
        )

    def test_get_item_by_slug(self):
        response = self.client.get(
            reverse('store:item_detail', kwargs={'slug': 'item-1'})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], self.item)
        self.assertEqual(response.context['item'].slug, self.item.slug)


class CategoryListViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        # Create a category and an item proxy
        self.category = Category.objects.create(
            name='Test Category', slug='test-category'
        )
        self.item = ItemProxy.objects.create(
            name='test_item', slug='test-item', category=self.category, image=self.test_gif
        )

    def test_status_code(self):
        response = self.client.get(
            reverse('store:category_list', args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('store:category_list', args=[self.category.slug])
        )
        self.assertTemplateUsed(response, 'store/category_items.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('store:category_list', args=[self.category.slug])
        )
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['items'].first(), self.item)