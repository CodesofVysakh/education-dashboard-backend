import uuid
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    student_name = models.CharField(max_length=255);
    courses = models.ManyToManyField('courses.Subject', related_name="subjects")
    enrollment_time = models.DateTimeField(db_index=True, auto_now_add=True)
    student_username = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'activity_enrollment'
        verbose_name = _('enrollment')
        verbose_name_plural = _('enrollment')
        ordering = ('-date_added',)

    def __str__(self):
        return self.student_name