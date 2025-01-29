from django.shortcuts import render
from rest_framework import generics

from .permissions import IsAdminOrReadOnly
from .serializers import ItemSerializer
from store.models import Item

class ItemsApiView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly] #custom permission class 
    queryset = Item.objects.select_related('category').order_by('id')
    serializer_class = ItemSerializer
