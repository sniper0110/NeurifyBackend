from django.contrib import admin
from .models import Customer, Task, ImageClass, ImageData

# Register your models here.
admin.site.register(Customer)
admin.site.register(Task)
admin.site.register(ImageClass)
admin.site.register(ImageData)
