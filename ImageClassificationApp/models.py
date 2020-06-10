from django.db import models
from django.contrib.auth.models import User

from .common import build_upload_to_path_for_images
# Create your models here.

class Customer(models.Model):

    site_user = models.OneToOneField(to=User, null=True, on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.username


class Task(models.Model):
    customer = models.ForeignKey(to=Customer, null=True, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=30, null=True)


class ImageClass(models.Model):
    task = models.ForeignKey(to=Task, null=True, on_delete=models.CASCADE)
    image_classname = models.CharField(max_length=30, null=True)


class ImageData(models.Model):

    imageclass = models.ForeignKey(to=ImageClass, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=build_upload_to_path_for_images)

