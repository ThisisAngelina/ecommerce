from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView


from .models import Category, Item, ItemProxy
from reviews.models import Review


class ItemsListView(ListView):
    model = Item
    context_object_name = 'items'
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx: # allow the items html to fish out the items from the items_hx special htmx 
            return "store/_partials/items_hx.html"
        return 'store/items.html'

def item_detail_view(request, slug):
    item = get_object_or_404(ItemProxy.objects.select_related('category'), slug=slug)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if item.reviews.filter(author=request.user).exists(): # if a user had already left a review
                messages.error(
                    request, 'Ooops! You have already left a review on this product!')
            else: # save the new review
                rating = request.POST.get('rating', 5)
                content = request.POST.get('content', '')
                if content:
                    item.reviews.create(rating=rating, content=content, author=request.user, item=item)
                    return redirect(request.path)
        else:  # the user is not logged in
            messages.error(
                request, 'You need to be logged in to leave a review.')

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