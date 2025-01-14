from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from .utils import generate_slug

class Category(models.Model):
    """
    Represents an item category
    """
    name = models.CharField(max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField('url', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name_plural = 'Categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        # display category parents
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(generate_slug() + 'pick' + self.name)  
        super(Category, self).save(*args, **kwargs)
    
    #def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})


class Item(models.Model):
    """
    Represents an item for sale
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    slug = models.SlugField('url', max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=9.99)
    image = models.ImageField(upload_to='items/items/%Y/%m/%d')
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    #def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})

class ItemManager(models.Manager):
    """
    Custom manager for the Item model.
    This manager filters the queryset to only include items that are available.

    """

    def get_queryset(self):
        return super(ItemManager, self).get_queryset().filter(availability=True)
                                                                                                                                    

class ItemProxy(Item):
    """
    Proxy for the Item model: the queryset returns only available items

    """
    objects = ItemManager()
    
    class Meta:
        proxy = True

