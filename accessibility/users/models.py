from django.contrib.gis.db import models
from helusers.models import AbstractUser
from django.contrib.postgres.fields import JSONField


# class Organization(models.Model):
#     name = models.CharField(max_length=32)
#     full_name = models.TextField(blank=True)
#     identifier = JSONField()

#     def __str__(self):
#         return self.full_name


class User(AbstractUser):
    pass
