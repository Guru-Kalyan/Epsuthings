from django.db import models
from django.conf import settings

class RecentActivity(models.Model):
    ACTIVITY_TYPES = (
        ('Blog', 'Blog'),
        ('Case Study', 'Case Study'),
        ('Inbox', 'Inbox'),
        ('Demo Request', 'Demo Request'),
    )
    
    activity_text = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='New') # e.g., Published, New, Updated
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.activity_text
