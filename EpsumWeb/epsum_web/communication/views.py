import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from common.views import AuthorizedAPIView as AuthAPIView, log_activity
from .models import Inbox, DemoRequest
from masters.models import IndustryType, InquiryType

class ReadInboxAPIView(View):
    def get(self, request, *args, **kwargs):
        try:
            inbox_id = request.GET.get('inbox_id')
            if inbox_id:
                obj = Inbox.objects.filter(id=inbox_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Inbox not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(inbox) for inbox in Inbox.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "inbox_id": obj.id,
            "sender": obj.sender,
            "email": obj.email,
            "mobile_no": obj.mobile_no,
            "company_name": obj.company_name,
            "job_title": obj.job_title,
            "inquiry_type": obj.inquiry_type.inquiry_type_name if obj.inquiry_type else None,
            "industry": obj.industry.industry_type_name if obj.industry else None,
            "message": obj.message,
            "read_status": obj.read_status,
            "date": obj.date
        }

@method_decorator(csrf_exempt, name='dispatch')
class CreateInboxAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                sender = data.get('sender')
                email = data.get('email')
                mobile_no = data.get('mobile_no')
                company_name = data.get('company_name')
                job_title = data.get('job_title')
                inquiry_type_id = data.get('inquiry_type')
                industry = data.get('industry')
                message = data.get('message')
                
                user = request.user
                if not sender or not email or not company_name or not inquiry_type_id:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                if inquiry_type_id:
                    inquiry = InquiryType.objects.filter(id=inquiry_type_id).first()
                    if not inquiry:
                        return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)
                    industry = IndustryType.objects.filter(id=industry).first()
                    if not industry:
                        return JsonResponse({"status": "failed", "msg": "Industry not found"}, status=400)
                    
                    inquiry_type = inquiry.inquiry_type
                    if inquiry_type == '1':
                        inbox = Inbox.objects.create(
                            sender=sender,
                            email=email,
                            mobile_no=mobile_no,
                            company_name=company_name,
                            job_title=job_title,
                            inquiry_type=inquiry,
                            industry=industry,
                            message=message
                        )
                        log_activity(f"Contact form from {inbox.sender} ({inbox.company_name})", "Inbox", "New")
                        return JsonResponse({"status": "success", "msg": "Inbox Created Successfully.", "id": inbox.id}, status=200)
                    elif inquiry_type == '2':
                        demo = DemoRequest.objects.create(
                            sender_name=sender,
                            company_name=company_name,
                            email=email,
                            mobile_no=mobile_no,
                            job_title=job_title,
                            inquiry_type=inquiry,
                            industry=industry,
                            message=message
                        )
                        log_activity(f"New demo request from {demo.sender_name} ({demo.company_name})", "Demo Request", "New")
                        return JsonResponse({"status": "success", "msg": "Demo Request Created Successfully.", "id": demo.id}, status=200)
                    else:
                        return JsonResponse({"status": "failed", "msg": "Inbox Type not found for selected Inquiry Type"}, status=400)
                else:
                    return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class UpdateInboxAPIView(AuthAPIView):
    def put(self, request, inbox_id,*args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                read_status = data.get('read_status')

                inbox = Inbox.objects.filter(id=inbox_id).first()
                if not inbox:
                    return JsonResponse({"status": "failed", "msg": "Inbox not found"}, status=400)

                inbox.read_status = read_status
                inbox.updated_by = self.user
                inbox.save()
                log_activity(f"Inbox message from {inbox.sender} marked as {'Read' if read_status == 'read' else 'Unread'}", "Inbox", "Updated")
                return JsonResponse({"status": "success", "msg": "Inbox Updated Successfully."}, status=200)
        
        except Inbox.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Inbox not found"}, status=400)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteInboxAPIView(AuthAPIView):
    def delete(self, request, inbox_id, *args, **kwargs):
        try:
            if not inbox_id:
                return JsonResponse({"status": "failed", "msg": "Inbox not found"}, status=400)

            inbox = Inbox.objects.filter(id=inbox_id).first()
            if not inbox:
                return JsonResponse({"status": "failed", "msg": "Inbox not found"}, status=400)

            inbox.delete()
            return JsonResponse({"status": "success", "msg": "Inbox Deleted Successfully."}, status=200)
        except Inbox.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Inbox not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class ReadDemoRequestAPIView(AuthAPIView):
    def get(self, request, *args, **kwargs):
        try:
            demo_request_id = request.GET.get('demo_request_id')
            if demo_request_id:
                obj = DemoRequest.objects.filter(id=demo_request_id).first()
                if not obj:
                    return JsonResponse({"status": "failed", "msg": "Demo Request not found"}, status=400)
                data = self.__serialize(obj)
                return JsonResponse({"status": "success", "data": data}, status=200)
            
            data = [self.__serialize(demo_request) for demo_request in DemoRequest.objects.all()]
            return JsonResponse({"status": "success", "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
    
    def __serialize(self, obj):
        return {
            "demo_request_id": obj.id,
            "sender_name": obj.sender_name,
            "company_name": obj.company_name,
            "email": obj.email,
            "mobile_no": obj.mobile_no,
            "job_title": obj.job_title,
            "inquiry_type": obj.inquiry_type.inquiry_type_name if obj.inquiry_type else None,
            "industry": obj.industry.industry_type_name if obj.industry else None,
            "message": obj.message,
            "date": obj.date,
            "req_status": obj.req_status
        }

@method_decorator(csrf_exempt, name='dispatch')
class CreateDemoRequestAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                sender_name = data.get('sender_name')
                company_name = data.get('company_name')
                email = data.get('email')
                mobile_no = data.get('mobile_no')
                job_title = data.get('job_title')
                inquiry_type = data.get('inquiry_type')
                industry = data.get('industry')
                message = data.get('message')
                
                if not sender_name or not company_name or not email or not industry:
                    return JsonResponse({"status": "failed", "msg": "Missing required fields"}, status=400)

                if inquiry_type:
                    inquiry = InquiryType.objects.filter(id=inquiry_type).first()
                    if not inquiry:
                        return JsonResponse({"status": "failed", "msg": "Inquiry Type not found"}, status=400)

                if industry:
                    industry = IndustryType.objects.filter(id=industry).first()
                    if not industry:
                        return JsonResponse({"status": "failed", "msg": "Industry Type not found"}, status=400)

                demo_request = DemoRequest.objects.create(
                    sender_name=sender_name,
                    company_name=company_name,
                    email=email,
                    mobile_no=mobile_no,
                    job_title=job_title,
                    inquiry_type=inquiry,
                    industry=industry,
                    message=message
                )
                return JsonResponse({"status": "success", "msg": "Demo Request Created Successfully.", "id": demo_request.id}, status=200)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class UpdateDemoRequestAPIView(AuthAPIView):
    def put(self, request, demo_request_id,*args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                req_status = data.get('req_status')

                demo_request = DemoRequest.objects.filter(id=demo_request_id).first()
                if not demo_request:
                    return JsonResponse({"status": "failed", "msg": "Demo Request not found"}, status=400)

                demo_request.req_status = req_status
                demo_request.updated_by = self.user
                demo_request.save()
                status_labels = {'1':'New', '2':'Scheduled', '3':'Completed', '4':'Cancelled'}
                log_activity(f"Demo request from {demo_request.sender_name} status updated to {status_labels.get(req_status, 'Updated')}", "Demo Request", status_labels.get(req_status, 'Updated'))
                return JsonResponse({"status": "success", "msg": "Demo Request Updated Successfully."}, status=200)
        
        except DemoRequest.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Demo Request not found"}, status=400)

        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

class DeleteDemoRequestAPIView(AuthAPIView):
    def delete(self, request, demo_request_id, *args, **kwargs):
        try:
            if not demo_request_id:
                return JsonResponse({"status": "failed", "msg": "Demo Request not found"}, status=400)

            demo_request = DemoRequest.objects.filter(id=demo_request_id).first()
            if not demo_request:
                return JsonResponse({"status": "failed", "msg": "Demo Request not found"}, status=400)

            demo_request.delete()
            return JsonResponse({"status": "success", "msg": "Demo Request Deleted Successfully."}, status=200)
        except DemoRequest.DoesNotExist as e:
            return JsonResponse({"status": "failed", "msg": "Demo Request not found"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": f"Error: {e}"}, status=400)

