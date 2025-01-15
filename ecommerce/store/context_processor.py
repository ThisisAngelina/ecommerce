from .models import Category


def categories(request):
    ''' Querries the DB and returns all the product categories: needed to display the categories in the base template '''
    categories = Category.objects.all()
    return {'categories' : categories}
                 