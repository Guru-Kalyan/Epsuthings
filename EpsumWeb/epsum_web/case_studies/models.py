from django.db import models
from django.utils.text import slugify

# Create your models here.
class CaseStudies(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
    
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    industry = models.ForeignKey("masters.IndustryType", on_delete=models.SET_NULL, null=True, blank=True)
    case_study_status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    overview = models.TextField()
    cover_image = models.ImageField(upload_to="case_studies/", null=True, blank=True)
    challenges = models.TextField(null=True, blank=True)
    solutions = models.TextField(null=True, blank=True)
    results = models.TextField(null=True, blank=True)

    key_metrics = models.JSONField(null=True, blank=True)
    meta_desc = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='case_studies_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='case_studies_updated_by')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "case_studies"
        ordering = ["-created_at"]


