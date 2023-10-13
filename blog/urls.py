from django.urls import path
from django.views.decorators.cache import cache_page
from blog.apps import BlogConfig
from django.conf import settings
from django.conf.urls.static import static
from blog.views import *


app_name = BlogConfig.name


urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)