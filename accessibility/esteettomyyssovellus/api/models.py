from django.db import models

# Create your models here.
class Form(models.Model):
    form_id = models.CharField(max_length=30)

