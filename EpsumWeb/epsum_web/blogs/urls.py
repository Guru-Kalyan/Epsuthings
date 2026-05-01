from django.urls import path
from . import views

urlpatterns = [
    path('read_blog/', views.ReadBlogAPIView.as_view(), name='read_blog'),
    path('create_blog/', views.CreateUpdateBlogAPIView.as_view(), name='create_blog'),
    path('update_blog/<int:blog_id>/', views.CreateUpdateBlogAPIView.as_view(), name='update_blog'),
    path('delete_blog/<int:blog_id>/', views.DeleteBlogAPIView.as_view(), name='delete_blog'),
]