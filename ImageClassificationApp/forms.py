from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


from .models import Customer, Task, ImageData, ImageClass

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

class ImageClassForm(ModelForm):

    class Meta:
        model = ImageClass
        fields = '__all__'

