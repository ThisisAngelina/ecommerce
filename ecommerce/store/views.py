from django.shortcuts import render, get_object_or_404

from .models import Category, Item, ItemProxy

def items_view(request):
    items = ItemProxy.objects.all()
    return render(request, 'store/items.html', {'items': items})

def item_detail_view(request, slug):
    item = get_object_or_404(ItemProxy, slug=slug)
    return render(request, 'store/item_detail.html', {'item': item})

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = ItemProxy.objects.select_related('category').filter(category=category)

    context = {'category': category, 'items': items}
    return render(request, 'store/category_items.html', context)

def search(request):
    return render(request, 'store/index.html')