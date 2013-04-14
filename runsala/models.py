from django.db import models
from django.conf import settings


class Repository(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class Secret(models.Model):
    path = models.CharField(max_length=255)
    data = models.TextField()


class Access(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    repository = models.ForeignKey(Repository)
    key = models.TextField()

    class Meta:
        unique_together = (('user', 'repository'),)
