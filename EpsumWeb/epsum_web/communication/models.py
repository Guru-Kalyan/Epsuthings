from django.db import models
from .backend.app import validate_email_address, mobile_validator

class Inbox(models.Model):
    class ReadStatus(models.TextChoices):
        UNREAD = 'unread', 'Unread'
        READ = 'read', 'Read'

    sender = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True, validators=[mobile_validator])
    company_name = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    inquiry_type = models.ForeignKey("masters.InquiryType", on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey("masters.IndustryType", on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    read_status = models.CharField(max_length=10, choices=ReadStatus.choices, default=ReadStatus.UNREAD)
    date = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='inboxes_updated_by')

    def save(self, *args, **kwargs):
        self.full_clean()  # triggers validators
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sender
    
    class Meta:
        db_table = "inboxes"
        ordering = ['-date']

class DemoRequest(models.Model):
    class ReqStatus(models.TextChoices):
        NEW = 'new', 'New'
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    sender_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True, validators=[mobile_validator])
    job_title = models.CharField(max_length=255, null=True, blank=True)
    inquiry_type = models.ForeignKey("masters.InquiryType", on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey("masters.IndustryType", on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    req_status = models.CharField(max_length=20, choices=ReqStatus.choices, default=ReqStatus.NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='demo_requests_updated_by')

    def save(self, *args, **kwargs):
        self.full_clean()  # triggers validators
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sender_name
    
    class Meta:
        db_table = "demo_requests"
        ordering = ['-date']
