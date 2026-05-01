from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.permissions.auth import Authentication, Authorization
from common.permissions.exceptions import AutheticationFailed, ImposterException, TokenExpired
from .models import RecentActivity
from blogs.models import Blog
from case_studies.models import CaseStudies
from communication.models import Inbox, DemoRequest

from django.shortcuts import render

class CORSAPIView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def options(self, request, *args, **kwargs):
        res = HttpResponse('', "application/json", status=200)
        res['Access-Control-Allow-Origin'] = '*'
        res["Access-Control-Allow-Headers"] = "*"
        res["Access-Control-Expose-Headers"] = "Authorization, user"
        res["Access-Control-Allow-Credentials"] = "true"
        res["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return res

class AuthorizedAPIView(Authorization, CORSAPIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method != "OPTIONS":
            try:
                self.authorize(request)
            except AutheticationFailed as e:
                return JsonResponse({"error": str(e)}, status=401)
            except ImposterException as e:
                return JsonResponse({"error": str(e)}, status=403)
            except TokenExpired as e:
                return JsonResponse({"error": str(e)}, status=401)

        return super().dispatch(request, *args, **kwargs)

class DashboardStatsAPIView(AuthorizedAPIView):
    def get(self, request, *args, **kwargs):
        try:
            blog_count = Blog.objects.filter(blog_status='published').count()
            cs_count = CaseStudies.objects.all().count()
            unread_inbox = Inbox.objects.filter(read_status='unread').count()
            demo_requests = DemoRequest.objects.all().count()
            
            return JsonResponse({
                "status": "success",
                "data": {
                    "blogs": blog_count,
                    "case_studies": cs_count,
                    "unread_inbox": unread_inbox,
                    "demo_requests": demo_requests
                }
            }, status=200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": str(e)}, status=400)

class RecentActivityAPIView(AuthorizedAPIView):
    def get(self, request, *args, **kwargs):
        try:
            activities = RecentActivity.objects.all()[:10]
            data = [{
                "text": a.activity_text,
                "type": a.activity_type,
                "date": a.date.strftime("%b %d, %Y"),
                "status": a.status
            } for a in activities]
            return JsonResponse({"status": "success", "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": str(e)}, status=400)

def log_activity(text, type, status='New'):
    RecentActivity.objects.create(
        activity_text=text,
        activity_type=type,
        status=status
    )


# Template Views
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html', {'active_page': 'dashboard'})

def admin_blogs(request):
    return render(request, 'admin/blogs.html', {'active_page': 'blogs'})

def admin_casestudies(request):
    return render(request, 'admin/case_studies.html', {'active_page': 'casestudies'})

def admin_inbox(request):
    return render(request, 'admin/inbox.html', {'active_page': 'inbox'})

def admin_demos(request):
    return render(request, 'admin/demos.html', {'active_page': 'demos'})

def admin_api_ref(request):
    return render(request, 'admin/api_ref.html', {'active_page': 'api'})

def login_view(request):
    return render(request, 'admin/login.html')

def register_view(request):
    return render(request, 'admin/register.html')

def error_404(request, exception):
    return render(request, 'admin/404.html', status=404)

def error_403(request, exception=None):
    return render(request, 'admin/403.html', status=403)
