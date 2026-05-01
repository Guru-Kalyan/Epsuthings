from django.urls import path
from . import views

urlpatterns = [
    path('read_blog_category/', views.ReadBlogCategoryAPIView.as_view(), name='read_blog_category'),
    path('create_blog_category/', views.CreateBlogCategoryAPIView.as_view(), name='create_blog_category'),
    path('update_blog_category/<int:blog_category_id>/', views.UpdateBlogCategoryAPIView.as_view(), name='update_blog_category'),
    path('delete_blog_category/<int:blog_category_id>/', views.DeleteBlogCategoryAPIView.as_view(), name='delete_blog_category'),
    path('read_industry_type/', views.ReadIndustryTypeAPIView.as_view(), name='read_industry_type'),
    path('create_industry_type/', views.CreateIndustryTypeAPIView.as_view(), name='create_industry_type'),
    path('update_industry_type/<int:industry_type_id>/', views.UpdateIndustryTypeAPIView.as_view(), name='update_industry_type'),
    path('delete_industry_type/<int:industry_type_id>/', views.DeleteIndustryTypeAPIView.as_view(), name='delete_industry_type'),
    path('read_inquiry_type/', views.ReadInquiryTypeAPIView.as_view(), name='read_inquiry_type'),
    path('create_inquiry_type/', views.CreateInquiryTypeAPIView.as_view(), name='create_inquiry_type'),
    path('update_inquiry_type/<int:inquiry_type_id>/', views.UpdateInquiryTypeAPIView.as_view(), name='update_inquiry_type'),
    path('delete_inquiry_type/<int:inquiry_type_id>/', views.DeleteInquiryTypeAPIView.as_view(), name='delete_inquiry_type'),
]

