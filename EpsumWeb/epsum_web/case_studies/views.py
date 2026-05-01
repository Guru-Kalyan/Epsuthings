import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError, transaction
from common.views import AuthorizedAPIView as AuthView, log_activity
from .models import CaseStudies
from masters.models import IndustryType

# Create your views here.
class ReadCaseStudiesAPIView(View):
    def get(self, request, *args, **kwargs):
        try:
            case_studies_id = request.GET.get('case_studies_id')
            slug = request.GET.get('slug')
            if case_studies_id:
                obj = CaseStudies.objects.filter(id=case_studies_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            if slug:
                obj = CaseStudies.objects.filter(slug=slug).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(case_studies) for case_studies in CaseStudies.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "case_studies_id": obj.id,
            "case_studies_title": obj.title,
            "slug": obj.slug,
            "industry": obj.industry.industry_type_name if obj.industry else None,
            "case_study_status": obj.case_study_status,
            "company_name": obj.company_name,
            "overview": obj.overview,
            "cover_image": obj.cover_image.url if obj.cover_image else None,
            "challenges": obj.challenges,
            "solutions": obj.solutions,
            "results": obj.results,
            "key_metrics": obj.key_metrics,
            "meta_desc": obj.meta_desc
        }

class CreateUpdateCaseStudiesAPIView(AuthView):
    def post(self, request, case_studies_id=None, *args, **kwargs):
        
        if request.POST.get('_method') == 'PUT' and case_studies_id:
            return self.put(request, case_studies_id, *args, **kwargs)
        
        try:
            with transaction.atomic():
                data = request.POST

                user = self.user
                title = data.get('title')
                slug = data.get('slug') or None
                industry = data.get('industry')
                case_study_status = data.get('case_study_status')
                company_name = data.get('company_name')
                overview = data.get('overview')
                cover_image = request.FILES.get('cover_image')
                challenges = data.get('challenges')
                solutions = data.get('solutions')
                results = data.get('results')
                key_metrics = data.get('key_metrics')
                meta_desc = data.get('meta_desc', None)

                if not title or not case_study_status or not industry or not overview:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)
                
                industry = IndustryType.objects.filter(id=industry).first()
                if not industry:
                    return JsonResponse({"status": "failed", "msg": " Invalid industry type"}, status=400)
                
                if key_metrics:
                    try:
                        key_metrics = json.loads(key_metrics)
                    except json.JSONDecodeError:
                        return JsonResponse({
                            "status": "failed",
                            "msg": "Invalid JSON format for key_metrics"
                        }, status=400)

                case_studies = CaseStudies.objects.create(
                    title=title,
                    slug=slug,
                    industry=industry,
                    case_study_status=case_study_status,
                    company_name=company_name,
                    overview=overview,
                    cover_image=cover_image,
                    challenges=challenges,
                    solutions=solutions,
                    results=results,
                    key_metrics=key_metrics,
                    meta_desc=meta_desc,
                    created_by=user
                )

                status_label = case_studies.case_study_status.title()
                log_activity(f"Case Study \"{case_studies.title}\" {case_studies.case_study_status}", "Case Study", status_label)

                return JsonResponse({"status": "success", "msg": "Case Studies Created Successfully.", "id": case_studies.id}, status=200)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def put(self, request, case_studies_id, *args, **kwargs):
        try:
            with transaction.atomic():
                if request.content_type.startswith('multipart/form-data'):
                    data = request.POST
                    cover_image = request.FILES.get('cover_image')
                else:
                    data = json.loads(request.body)
                    cover_image = None

                user = self.user
                title = data.get('title')
                slug = data.get('slug') or None
                industry = data.get('industry')
                case_study_status = data.get('case_study_status')
                company_name = data.get('company_name')
                overview = data.get('overview')
                
                challenges = data.get('challenges')
                solutions = data.get('solutions')
                results = data.get('results')
                key_metrics = data.get('key_metrics')
                meta_desc = data.get('meta_desc')

                if industry:
                    industry = IndustryType.objects.filter(id=industry).first()
                    if not industry:
                        return JsonResponse({"status": "failed", "msg": " Invalid industry type"}, status=400)

                if key_metrics:
                    try:
                        key_metrics = json.loads(key_metrics)
                    except json.JSONDecodeError:
                        return JsonResponse({
                            "status": "failed",
                            "msg": "Invalid JSON format for key_metrics"
                        }, status=400)

                if not case_studies_id:
                    return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)

                case_studies = CaseStudies.objects.filter(id=case_studies_id).first()
                if not case_studies:
                    return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)

                case_studies.title = title if title else case_studies.title
                case_studies.slug = slug if slug else case_studies.slug
                case_studies.industry = industry if industry else case_studies.industry
                case_studies.case_study_status = case_study_status if case_study_status else case_studies.case_study_status
                case_studies.company_name = company_name if company_name else case_studies.company_name
                case_studies.overview = overview if overview else case_studies.overview
                case_studies.cover_image = cover_image if cover_image else case_studies.cover_image
                case_studies.challenges = challenges if challenges else case_studies.challenges
                case_studies.solutions = solutions if solutions else case_studies.solutions
                case_studies.results = results if results else case_studies.results
                case_studies.key_metrics = key_metrics if key_metrics else case_studies.key_metrics
                case_studies.meta_desc = meta_desc if meta_desc else case_studies.meta_desc
                case_studies.updated_by = user
                case_studies.save()

                status_label = case_studies.case_study_status.title()
                log_activity(f"Case Study \"{case_studies.title}\" updated", "Case Study", status_label)

                return JsonResponse({"status": "success", "msg": "Case Studies Updated Successfully"}, status=200)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except CaseStudies.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteCaseStudiesAPIView(AuthView):
    def delete(self, request, case_studies_id, *args, **kwargs):
        try:
            if not case_studies_id:
                return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)

            case_studies = CaseStudies.objects.filter(id=case_studies_id).first()
            if not case_studies:
                return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)

            case_studies.delete()
            return JsonResponse({"status": "success", "msg": "Case Studies Deleted Successfully."}, status=200)
        except CaseStudies.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Case Studies not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    

