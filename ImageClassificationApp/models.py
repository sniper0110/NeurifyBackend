from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    site_user = models.OneToOneField(to=User, null=True, on_delete=models.DO_NOTHING)


class Task(models.Model):
    customer = models.ForeignKey(to=Customer, null=True, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=30, null=True)


class ImageData(models.Model):

    task = models.ForeignKey(to=Task, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='data/')

