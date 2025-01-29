from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from store.models import Item, Category
from reviews.models import Review

User = get_user_model()

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'category', 'name', 'brand', 'price', 'description', 'image', 'availability', 'created_at', 'updated_at']