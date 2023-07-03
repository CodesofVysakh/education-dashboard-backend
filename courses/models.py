import uuid
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    name = models.CharField(max_length=255);
    duration = models.CharField(max_length=128, null=True, blank=True);
    description = models.TextField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'courses_subject'
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        ordering = ('name',)

    def __str__(self):
        return self.name