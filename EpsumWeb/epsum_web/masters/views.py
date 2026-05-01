import json
from django.shortcuts import render
from django.views import View
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from common.views import AuthorizedAPIView as AuthAPIView
from .models import BlogCategory, IndustryType, InquiryType


class ReadBlogCategoryAPIView(AuthAPIView):
    def get(self, request, *args, **kwargs):
        try:
            category_id = request.GET.get('category_id')
            if category_id:
                obj = BlogCategory.objects.filter(id=category_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(category) for category in BlogCategory.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "category_id": obj.id,
            "category_name": obj.category_name,
            "description": obj.description
        }

class CreateBlogCategoryAPIView(AuthAPIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                category_name = data.get('category_name')
                description = data.get('description')
                user = self.user
                if not category_name:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                category = BlogCategory.objects.create(
                    category_name=category_name,
                    description=description,
                    created_by=user
                )
                return JsonResponse({"status": "success", "msg": "Blog Category Created Successfully.", "id": category.id}, status=200)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Blog Category already exists"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class UpdateBlogCategoryAPIView(AuthAPIView):
    def put(self, request, category_id, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                category_name = data.get('category_name')
                description = data.get('description')
                user = self.user

                if not category_name:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                category = BlogCategory.objects.filter(id=category_id).first()
                if not category:
                    return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)

                category.category_name = category_name if category_name else category.category_name
                category.description = description if description else category.description
                category.updated_by = user
                category.save()
                return JsonResponse({"status": "success", "msg": "Blog Category Updated Successfully."}, status=200)
        
        except BlogCategory.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteBlogCategoryAPIView(AuthAPIView):
    def delete(self, request, category_id, *args, **kwargs):
        try:
            if not category_id:
                return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)

            category = BlogCategory.objects.filter(id=category_id).first()
            if not category:
                return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)

            category.delete()
            return JsonResponse({"status": "success", "msg": "Blog Category Deleted Successfully."}, status=200)
        except BlogCategory.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Blog Category not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class ReadIndustryTypeAPIView(AuthAPIView):
    def get(self, request, *args, **kwargs):
        try:
            industry_type_id = request.GET.get('industry_type_id')
            if industry_type_id:
                obj = IndustryType.objects.filter(id=industry_type_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(industry) for industry in IndustryType.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "industry_type_id": obj.id,
            "industry_type_name": obj.industry_type_name,
            "description": obj.description
        }

class CreateIndustryTypeAPIView(AuthAPIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                industry_type_name = data.get('industry_type_name')
                description = data.get('description')
                user = self.user

                if not industry_type_name:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                industry = IndustryType.objects.create(
                    industry_type_name=industry_type_name,
                    description=description,
                    created_by=user
                )
                return JsonResponse({"status": "success", "msg": "Industry Type Created Successfully.", "id": industry.id}, status=200)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Industry Type already exists"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class UpdateIndustryTypeAPIView(AuthAPIView):
    def put(self, request, industry_type_id, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                industry_type_name = data.get('industry_type_name')
                description = data.get('description')
                user = self.user

                if not industry_type_name:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                industry = IndustryType.objects.filter(id=industry_type_id).first()
                if not industry:
                    return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)

                industry.industry_type_name = industry_type_name if industry_type_name else industry.industry_type_name
                industry.description = description if description else industry.description
                industry.updated_by = user
                industry.save()
                return JsonResponse({"status": "success", "msg": "Industry Type Updated Successfully."}, status=200)
        
        except IndustryType.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteIndustryTypeAPIView(AuthAPIView):
    def delete(self, request, industry_type_id, *args, **kwargs):
        try:
            if not industry_type_id:
                return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)

            industry = IndustryType.objects.filter(id=industry_type_id).first()
            if not industry:
                return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)

            industry.delete()
            return JsonResponse({"status": "success", "msg": "Industry Type Deleted Successfully."}, status=200)
        except IndustryType.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class ReadInquiryTypeAPIView(AuthAPIView):
    def get(self, request, *args, **kwargs):
        try:
            inquiry_type_id = request.GET.get('inquiry_type_id')
            if inquiry_type_id:
                obj = InquiryType.objects.filter(id=inquiry_type_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Enquiry Type not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(enquiry) for enquiry in InquiryType.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "inquiry_type_id": obj.id,
            "inquiry_type_name": obj.inquiry_type_name,
            "description": obj.description,
            "inquiry_type": obj.inquiry_type
        }

class CreateInquiryTypeAPIView(AuthAPIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                inquiry_type_name = data.get('inquiry_type_name')
                description = data.get('description')
                inquiry_type = data.get('inquiry_type')

                if not inquiry_type_name:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                inquiry = InquiryType.objects.create(
                    inquiry_type_name=inquiry_type_name,
                    description=description,
                    inquiry_type=inquiry_type,
                    created_by=self.user
                )
                return JsonResponse({"status": "success", "msg": "Inquiry Type Created Successfully.", "id": inquiry.id}, status=200)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Inquiry Type already exists"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class UpdateInquiryTypeAPIView(AuthAPIView):
    def put(self, request, inquiry_type_id, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                inquiry_type_name = data.get('inquiry_type_name')
                description = data.get('description')
                inquiry_type = data.get('inquiry_type')
                user = self.user

                inquiry = InquiryType.objects.filter(id=inquiry_type_id).first()
                if not inquiry:
                    return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)

                inquiry.inquiry_type_name = inquiry_type_name if inquiry_type_name else inquiry.inquiry_type_name
                inquiry.description = description if description else inquiry.description
                inquiry.inquiry_type = inquiry_type if inquiry_type else inquiry.inquiry_type
                inquiry.updated_by = user
                inquiry.save()
                return JsonResponse({"status": "success", "msg": "Inquiry Type Updated Successfully."}, status=200)
        except InquiryType.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteInquiryTypeAPIView(AuthAPIView):
    def delete(self, request, inquiry_type_id, *args, **kwargs):
        try:
            if not inquiry_type_id:
                return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)

            enquiry = InquiryType.objects.filter(id=inquiry_type_id).first()
            if not enquiry:
                return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)

            enquiry.delete()
            return JsonResponse({"status": "success", "msg": "Inquiry Type Deleted Successfully."}, status=200)
        except InquiryType.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

