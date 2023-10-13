from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'views')
    list_filter = ('views',)
    search_fields = ('title',)
