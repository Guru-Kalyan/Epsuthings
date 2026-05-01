from django.urls import path
from . import views

urlpatterns = [
    path('read_inbox/', views.ReadInboxAPIView.as_view(), name='read_inbox'),
    path('create_inbox/', views.CreateInboxAPIView.as_view(), name='create_inbox'),
    path('update_inbox/<int:inbox_id>/', views.UpdateInboxAPIView.as_view(), name='update_inbox'),
    path('delete_inbox/<int:inbox_id>/', views.DeleteInboxAPIView.as_view(), name='delete_inbox'),
    path('read_demo_request/', views.ReadDemoRequestAPIView.as_view(), name='read_demo_request'),
    path('create_demo_request/', views.CreateDemoRequestAPIView.as_view(), name='create_demo_request'),
    path('update_demo_request/<int:demo_request_id>/', views.UpdateDemoRequestAPIView.as_view(), name='update_demo_request'),
    path('delete_demo_request/<int:demo_request_id>/', views.DeleteDemoRequestAPIView.as_view(), name='delete_demo_request'),
]

