from django.db import models

class BlogCategory(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='blog_categories_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='blog_categories_updated_by')

    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = 'blog_categories'

class IndustryType(models.Model):
    industry_type_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='industry_types_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='industry_types_updated_by')

    def __str__(self):
        return self.industry_type_name
    
    class Meta:
        db_table = 'industry_types'

class InquiryType(models.Model):
    class TypeChoices(models.TextChoices):
        INBOX = '1', 'Inbox'
        DEMO = '2', 'Demo'
    inquiry_type_name = models.CharField(max_length=255, unique=True)
    inquiry_type = models.CharField(max_length=25, choices=TypeChoices.choices, default=TypeChoices.INBOX)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='enquiry_types_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,related_name='enquiry_types_updated_by')

    def __str__(self):
        return self.inquiry_type_name
    
    class Meta:
        db_table = 'inquiry_types'
