import json
from django.shortcuts import render
from django.views import View
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from common.views import AuthorizedAPIView as AuthAPIView, log_activity
from .models import Blog
from masters.models import BlogCategory

# Create your views here.
class ReadBlogAPIView(View):
    def get(self, request, *args, **kwargs):
        try:
            blog_id = request.GET.get('blog_id')
            slug = request.GET.get('slug')
            if blog_id:
                obj = Blog.objects.filter(id=blog_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            if slug:
                obj = Blog.objects.filter(slug=slug).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(blog) for blog in Blog.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "blog_id": obj.id,
            "blog_title": obj.title,
            "slug": obj.slug,
            "category": obj.category.category_name if obj.category else None,
            "blog_status": obj.blog_status,
            "author": obj.author,
            "publish_date": obj.publish_date,
            "blog_desc": obj.blog_desc,
            "content": obj.content,
            "feature_image": obj.feature_image.url if obj.feature_image else None,
            "meta_desc": obj.meta_desc
        }

class CreateUpdateBlogAPIView(AuthAPIView):
    def post(self, request, blog_id=None,*args, **kwargs):
        if request.POST.get('_method') == 'PUT' and blog_id:
            return self.put(request, blog_id, *args, **kwargs)
        
        try:
            with transaction.atomic():
                data = request.POST

                user = self.user
                title = data.get('title')
                slug = data.get('slug')
                category = data.get('category')
                blog_status = data.get('blog_status')
                author = data.get('author')
                publish_date = data.get('publish_date')
                blog_desc = data.get('blog_desc')
                content = data.get('content')
                feature_image = request.FILES.get('feature_image')
                meta_desc = data.get('meta_desc')

                category = BlogCategory.objects.filter(id=category).first()
                if not category:
                    return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)

                if not title or not blog_status or not category or not blog_desc or not content:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                blog = Blog.objects.create(
                    title=title,
                    slug=slug,
                    category=category,
                    blog_status=blog_status,
                    author=author,
                    publish_date=publish_date,
                    blog_desc=blog_desc,
                    content=content,
                    feature_image=feature_image,
                    meta_desc=meta_desc,
                    created_by=user
                )

                status_label = blog.blog_status.title()
                log_activity(f"Blog \"{blog.title}\" {blog.blog_status}", "Blog", status_label)

                return JsonResponse({"status": "success", "msg": "Blog Created Successfully.", "id": blog.id}, status=201)
            
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def put(self, request, blog_id, *args, **kwargs):
        try:
            with transaction.atomic():
                if request.content_type.startswith('multipart/form-data'):
                    data = request.POST
                    feature_image = request.FILES.get('feature_image')
                else:
                    data = json.loads(request.body)
                    feature_image = None

                user = self.user
                title = data.get('title')
                slug = data.get('slug')
                category = data.get('category')
                blog_status = data.get('blog_status')
                author = data.get('author')
                publish_date = data.get('publish_date')
                blog_desc = data.get('blog_desc')
                content = data.get('content')
                
                meta_desc = data.get('meta_desc')

                if not blog_id:
                    return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)
                
                if category:
                    category = BlogCategory.objects.filter(id=category).first()
                    if not category:
                        return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)

                blog = Blog.objects.filter(id=blog_id).first()
                if not blog:
                    return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)

                blog.title = title if title else blog.title
                blog.slug = slug  if slug else blog.slug
                blog.category = category if category else blog.category
                blog.blog_status = blog_status  if blog_status else blog.blog_status
                blog.author = author if author else blog.author
                blog.publish_date = publish_date if publish_date else blog.publish_date
                blog.blog_desc = blog_desc if blog_desc else blog.blog_desc
                blog.content = content if content else blog.content
                blog.feature_image = feature_image if feature_image else blog.feature_image
                blog.meta_desc = meta_desc if meta_desc else blog.meta_desc
                blog.updated_by = user
                blog.save()

                status_label = blog.blog_status.title()
                log_activity(f"Blog \"{blog.title}\" updated", "Blog", status_label)

                return JsonResponse({"status": "success", "msg": "Blog Updated Successfully."}, status=200)
        except Blog.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteBlogAPIView(AuthAPIView):
    def delete(self, request, blog_id, *args, **kwargs):
        try:
            if not blog_id:
                return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)

            blog = Blog.objects.filter(id=blog_id).first()
            if not blog:
                return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)

            blog.delete()
            return JsonResponse({"status": "success", "msg": "Blog Deleted Successfully."}, status=200)
        except Blog.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Blog not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
