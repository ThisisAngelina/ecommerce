from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from store.models import Item

User = get_user_model()

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)

    street_name_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    zip_code = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return str(self.city) +  ' , '  + str(self.country)

class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True) # users can place orders without being authenticated
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                amount__gte=0), name='amount_gte_0'), # validate that the order amount cannot be smaller than 0
        ]

    def __str__(self):
        return "Order" + str(self.id)

    def get_absolute_url(self):
        return reverse("payment:order_detail", kwargs={"pk": self.pk})

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())


    @property
    def get_discount(self):
        if (total_cost := self.get_total_cost_before_discount()) and self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)


    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount() - self.get_discount
        return total_cost 
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1)
    

    class Meta:
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(check=models.Q(
                quantity__gt=0), name='quantity_gte_0'), # validate that the ordered quantity is greater than 0
        ]

    def __str__(self):
        return "OrderItem" + str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    @property
    def total_cost(self):
        return self.price * self.quantity

    @classmethod
    def get_total_quantity_for_product(cls, item):
        return cls.objects.filter(item=item).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    @staticmethod
    def get_average_price():
        return OrderItem.objects.aggregate(average_price=models.Avg('price'))['average_price']