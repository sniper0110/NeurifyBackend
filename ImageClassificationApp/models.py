from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    site_user = models.OneToOneField(to=User, null=True, on_delete=models.DO_NOTHING)



class ImageData(models.Model):

    customer = models.ForeignKey(to=Customer, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='data/')

