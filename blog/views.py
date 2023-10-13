from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blogs')
    extra_context = {'title': 'Создание статьи'}


class BlogListView(ListView):
    model = Blog
    extra_context = {'title': 'Блог'}


class BlogDetailView(DetailView):
    model = Blog
    extra_context = {'title': 'Статья'}

    def get_object(self, queryset=None):
        """Подсчет просмотров"""
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    extra_context = {'title': 'Редактирование статьи'}

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', args=(self.object.id,))


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs')
    extra_context = {'title': 'Удаление статьи'}
