import uuid
from model_utils import Choices

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _



# Create your models here.
PROFILE_ROLE_CHOICES = Choices(
    ('admin', 'admin', _('Admin')),
    ('student', 'student', _('Student')),
)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    role = models.CharField(max_length=128, default=PROFILE_ROLE_CHOICES.student)

    def save(self, *args, **kwargs):
        user = self.user
        
        if self.role == 'student':
            customer_group, created = Group.objects.get_or_create(name='student')
            customer_group.user_set.add(user)

        super(Profile, self).save(*args, **kwargs)

    class Meta:
        db_table = 'accounts_profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        ordering = ('name',)

    def __str__(self):
        return self.name