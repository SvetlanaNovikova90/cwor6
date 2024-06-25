from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from blog.forms import BlogForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс для создания блоговой записи
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:content')
    permission_required = 'blog.add_blog'


class BlogListView(LoginRequiredMixin, ListView):
    """
    Класс для создания списка блоговых записей
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_list.html'


class BlogManagementListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Класс для просмотра списка блоговых записей только контент-менеджером
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_management.html'
    permission_required = 'blog.add_blog'


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс позволяет редактировать запись
    """
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    permission_required = 'blog.change_blog'

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    template_name = 'blog/blog_confirm_delete.html'
    permission_required = 'blog.delete_blog'

