from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, \
    BlogManagementListView

app_name = 'blog'

urlpatterns = [
    path('create/', BlogCreateView.as_view(template_name='blog_form.html'), name='create'),
    path('', cache_page(60)(BlogListView.as_view(template_name='blog_list.html')), name='list'),
    path('blog_management/', BlogManagementListView.as_view(template_name='blog/blog_management.html'), name='content'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view(template_name='blog/blog_detail.html')), name='view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(template_name='blog/blog_form.html'), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(template_name='blog/blog_confirm_delete.html'), name='delete'),
]