"""
URL configuration for epsum_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from common import views as common_views

def index(request):
    return HttpResponse("<div><h1>Epsum Web Backend !!</h1></div>")

urlpatterns = [
    path('admin_django/', admin.site.urls), # Rename original admin to avoid conflict
    path('', index, name='index'),
    
    # Custom Admin Pages
    path('admin/dashboard/', common_views.admin_dashboard, name='admin_dashboard'),
    path('admin/blogs/', common_views.admin_blogs, name='admin_blogs'),
    path('admin/casestudies/', common_views.admin_casestudies, name='admin_casestudies'),
    path('admin/inbox/', common_views.admin_inbox, name='admin_inbox'),
    path('admin/demos/', common_views.admin_demos, name='admin_demos'),
    path('admin/api-ref/', common_views.admin_api_ref, name='admin_api_ref'),
    
    # Auth Pages
    path('login/', common_views.login_view, name='login'),
    path('register/', common_views.register_view, name='register'),

    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
    path('blogs/', include('blogs.urls')),
    path('case_studies/', include('case_studies.urls')),
    path('masters/', include('masters.urls')),
    path('communication/', include('communication.urls')),
    
    # Internal Admin APIs
    path('api/dashboard-stats/', common_views.DashboardStatsAPIView.as_view(), name='dashboard_stats_api'),
    path('api/recent-activity/', common_views.RecentActivityAPIView.as_view(), name='recent_activity_api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'common.views.error_404'
handler403 = 'common.views.error_403'

