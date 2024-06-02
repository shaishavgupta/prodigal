from django.db import models

class TagCount(models.Model):
    tag = models.CharField(max_length=255, unique=True, null=False, blank=False)
    count = models.IntegerField(default=1, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['tag'], name='tag_count_idx', condition=models.Q(count__gt=10)),
        ]