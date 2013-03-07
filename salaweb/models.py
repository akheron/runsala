from django.db import models
from django.conf import settings


class Access(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    repository = models.CharField(max_length=255)
    key = models.TextField()

    class Meta:
        unique_together = (('user', 'repository'),)
