from django.urls import path
from . import views

urlpatterns = [
    path('read_case_study/', views.ReadCaseStudiesAPIView.as_view(), name='read_case_study'),
    path('create_case_study/', views.CreateUpdateCaseStudiesAPIView.as_view(), name='create_case_study'),
    path('update_case_study/<int:case_study_id>/', views.CreateUpdateCaseStudiesAPIView.as_view(), name='update_case_study'),
    path('delete_case_study/<int:case_study_id>/', views.DeleteCaseStudiesAPIView.as_view(), name='delete_case_study'),
]