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

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','rating', 'content', 'author', 'created','item'] # the client sends item_id, rating and content via a POST request
        read_only_fields = ['id', 'author', 'created']

class ItemDetailSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        many=False,
        slug_field="name",
        queryset=Category.objects.all()
    )
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ["id", "name", "slug", "brand", "category", "price",
                  "image", "availability", "created_at", "updated_at", "reviews"]

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        user = User(
            email=email,
            username=username,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user