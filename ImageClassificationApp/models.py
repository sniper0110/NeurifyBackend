from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

import os

from .common import build_upload_to_path_for_images, path_for_model_artifacts_zip_upload, path_for_training_history_npy_upload

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
    creation_date = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.task_name


class ImageClass(models.Model):
    task = models.ForeignKey(to=Task, null=True, on_delete=models.CASCADE)
    image_classname = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.image_classname

    def get_all_images_of_class(self):
        return ImageData.objects.filter(imageclass=self)


class ImageData(models.Model):

    imageclass = models.ForeignKey(to=ImageClass, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=build_upload_to_path_for_images)


CLASSIFICATION_MODELS= (
    ('inceptionv3', 'InceptionV3'),
    ('vgg16', 'VGG16')
)

class ClassificationDeepLearningModel(models.Model):

    task = models.OneToOneField(Task, null=True, on_delete=models.CASCADE)
    classification_model_architecture = models.CharField(max_length=200, null=True, choices=CLASSIFICATION_MODELS)

    trained_model_file = models.FileField(blank=True, null=True, upload_to=path_for_model_artifacts_zip_upload)
    history_of_model_training = models.FileField(blank=True, null=True, upload_to=path_for_training_history_npy_upload)

    def set_trained_model_file(self, model_file_path):
        with open(model_file_path, "rb") as file:
            self.trained_model_file.save(os.path.basename(model_file_path), File(file))

    def set_history_file(self, history_file):
        with open(history_file, "rb") as file:
            self.history_of_model_training.save(os.path.basename(history_file), File(file))

    def __str__(self):
        return self.classification_model_architecture


class DeepLearningModelArtifacts(models.Model):
    classification_deeplearning_model = models.ForeignKey(ClassificationDeepLearningModel, on_delete=models.CASCADE, null=True)





