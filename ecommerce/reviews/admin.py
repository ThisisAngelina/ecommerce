from django.contrib import admin

from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['item', 'rating', 'content', 'author', 'created']

admin.site.register(Review, ReviewAdmin)
