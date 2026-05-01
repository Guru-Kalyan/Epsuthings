from django.db import models
from django.utils.text import slugify

# Create your models here.
class Blog(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        "masters.BlogCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    blog_status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    author = models.CharField(max_length=255)

    publish_date = models.DateField(null=True, blank=True)

    blog_desc = models.TextField()
    content = models.TextField(help_text="HTML content")

    feature_image = models.ImageField(
        upload_to="blogs/",
        null=True,
        blank=True
    )

    meta_desc = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='blogs_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='blogs_updated_by')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blogs"
        ordering = ["-created_at"]
