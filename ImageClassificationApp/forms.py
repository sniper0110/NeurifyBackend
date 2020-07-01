from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

from .models import Customer, Task, ImageData, ImageClass, ClassificationDeepLearningModel

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

class TaskFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        '''
        self.layout = Layout(
            'favorite_color',
            'favorite_food',
        )
        '''
        self.render_required_fields = True




class ImageClassForm(ModelForm):

    class Meta:
        model = ImageClass
        fields = '__all__'

class ImageClassFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True


class ImageDataForm(ModelForm):

    class Meta:
        model = ImageData
        fields = '__all__'


class ClassificationDeepLearningModelForm(ModelForm):

    class Meta:
        model = ClassificationDeepLearningModel
        fields = '__all__'