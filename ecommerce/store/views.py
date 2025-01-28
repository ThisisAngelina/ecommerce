from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView


from .models import Category, Item, ItemProxy


class ItemsListView(ListView):
    model = Item
    context_object_name = 'items'
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx: # allow the items html to fish out the items from the items_hx special htmx 
            return "store/_partials/items_hx.html"
        return 'store/items.html'

def item_detail_view(request, slug):
    item = get_object_or_404(ItemProxy, slug=slug)
    return render(request, 'store/item_detail.html', {'item': item})

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = ItemProxy.objects.select_related('category').filter(category=category)
    context = {'category': category, 'items': items}
    return render(request, 'store/category_items.html', context)

def search(request):
    query = request.GET.get('q')
    items = ItemProxy.objects.filter(name__icontains=query).distinct()

    if not query or not items:
        return redirect('store:items')
    
    return render(request, 'store/search_results.html', {'items': items})