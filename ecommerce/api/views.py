from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminOrReadOnly
from .serializers import ItemSerializer, ItemDetailSerializer, ReviewSerializer
from .pagination import StandardResultsSetPagination
from store.models import Item
from reviews.models import Review

class ItemsApiView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly] #custom permission class 
    pagination_class = StandardResultsSetPagination
    queryset = Item.objects.select_related('category').order_by('id')
    serializer_class = ItemSerializer


class ItemDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    lookup_field = "pk"


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        item_id = self.request.data.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        existing_review = Review.objects.filter(
            item=item, author=self.request.user).exists()
        if existing_review:
            raise ValidationError("You have already left a review for this product.")

        serializer.save(author=self.request.user, item=item)