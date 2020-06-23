from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user
from .forms import UserForm, ImageDataForm, ClassificationDeepLearningModelForm
from .models import Customer, Task, ImageClass, ImageData, ClassificationDeepLearningModel
from .validators import image_is_valid
from .deep_learning.inceptionv3 import run_training

# Create your views here.

@unauthenticated_user
def login_page(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"email is : {email}")
        print(f"password is : {password}")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user=user)
            print('login was successful!')
            return redirect('/home')

    return render(request, 'ImageClassificationApp/login_page.html')


@unauthenticated_user
def register_page(request):

    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/login')

    context = {'form': form}
    return render(request, 'ImageClassificationApp/register_page.html', context=context)


def logout_user(request):

    logout(request)
    return redirect('/login')


@login_required(login_url='ImageClassificationApp:login_page')
def home(request):

    return render(request, 'ImageClassificationApp/home.html')


@login_required(login_url='ImageClassificationApp:login_page')
def adding_task(request):

    TaskFormset = inlineformset_factory(Customer, Task, fields=('task_name',), extra=1)
    formset = TaskFormset(queryset=Task.objects.none(), instance=request.user.customer)

    if request.method == 'POST':

        formset = TaskFormset(request.POST, instance=request.user.customer)
        task_name = formset.cleaned_data[0]['task_name']

        #if task_name in [name.task_name for name in Task.objects.all()]:
        if task_name in [usertask.task_name for usertask in request.user.customer.task_set.all()]:
            messages.warning(request, "Task name already exists! Please choose another name!")
            context = {'formset': formset}
            return render(request, 'ImageClassificationApp/image_classification_content.html', context=context)

        if formset.is_valid():
            saved_formset = formset.save()
            return redirect(f'/home/image_classification/{saved_formset[0].pk}')

    context = {'formset': formset}
    return render(request, 'ImageClassificationApp/image_classification_content.html', context=context)


@login_required(login_url='ImageClassificationApp:login_page')
def adding_imageclass(request, pk):

    task_from_pk = Task.objects.get(pk=pk)
    imageclasses_already_in_task = [imgclass.image_classname for imgclass in task_from_pk.imageclass_set.all()]

    ImageClassFormset = inlineformset_factory(Task, ImageClass, fields=('image_classname',), extra=1)
    formset = ImageClassFormset(queryset=ImageClass.objects.none(), instance=task_from_pk)

    if request.method == 'POST':

        formset = ImageClassFormset(request.POST, instance=task_from_pk)
        classname = formset.cleaned_data[0]['image_classname']

        if classname in imageclasses_already_in_task:
            messages.warning(request, "This class already exists! Please choose another name!")
            context = {'formset': formset, 'task': task_from_pk,
                       'imageclasses_already_in_task': imageclasses_already_in_task}
            return render(request, 'ImageClassificationApp/image_classes_form.html', context=context)

        if formset.is_valid():
            instances = formset.save()
            pk_imageclass = instances[0].pk
            return redirect(f'/home/image_classification/{pk}/{pk_imageclass}')

    context = {'formset': formset, 'task': task_from_pk, 'imageclasses_already_in_task': imageclasses_already_in_task}
    return render(request, 'ImageClassificationApp/image_classes_form.html', context=context)


@login_required(login_url='ImageClassificationApp:login_page')
def adding_images(request, pk1, pk2):

    imageclass_from_pk = ImageClass.objects.get(pk=pk2)
    task = Task.objects.get(pk=pk1)

    if request.method == 'POST':

        if 'done' in request.POST:
            # TODO: is this the best way to upload multiple images?
            for file in request.FILES.getlist('images'):

                if image_is_valid(file):
                    ImageData.objects.create(imageclass=imageclass_from_pk, image=file)
                    messages.success(request, "Image has been successfully uploaded")
                else:
                    messages.error(request, "File type or extension not supported (only : png, jpg, jpeg are supported!)")

            return render(request, 'ImageClassificationApp/task_details_page.html')

        elif 'add_another_class' in request.POST:
            # TODO: is this the best way to upload multiple images?
            for file in request.FILES.getlist('images'):

                if image_is_valid(file):
                    ImageData.objects.create(imageclass=imageclass_from_pk, image=file)
                    messages.success(request, "Image has been successfully uploaded")
                else:
                    messages.error(request, "File type or extension not supported (only : png, jpg, jpeg are supported!)")

            return redirect(f'/home/image_classification/{pk1}')

    context = {'task': task, 'imageclass': imageclass_from_pk}
    return render(request, 'ImageClassificationApp/images_upload_form.html', context=context)


@login_required(login_url='ImageClassificationApp:login_page')
def classification_training(request):

    last_added_task = request.user.customer.task_set.last()
    image_classes = last_added_task.imageclass_set.all()
    class_to_images_dict = dict()

    for imageclass in image_classes:
        imagedata_set = imageclass.imagedata_set.all()
        class_to_images_dict.update({imageclass:imagedata_set})

    ClassificationDeepLearningModelFormset = inlineformset_factory(Task, ClassificationDeepLearningModel, fields=('classification_model',), extra=1)
    formset = ClassificationDeepLearningModelFormset(queryset=ClassificationDeepLearningModel.objects.none(), instance=last_added_task)

    if request.method == 'POST':
        formset = ClassificationDeepLearningModelFormset(request.POST, instance=last_added_task)
        if formset.is_valid():
            formset.save()

            return redirect(reverse('ImageClassificationApp:pretraining_summary'))


    context = {'last_task':last_added_task, 'image_classes': image_classes,
               "class_to_images_dict": class_to_images_dict, 'formset':formset}
    return render(request, 'ImageClassificationApp/classification_training_page.html', context=context)


def pretraining_summary(request):

    last_added_task = request.user.customer.task_set.last()
    image_classes = last_added_task.imageclass_set.all()
    class_to_images_dict = dict()

    for imageclass in image_classes:
        imagedata_set = imageclass.imagedata_set.all()
        class_to_images_dict.update({imageclass:imagedata_set})

    classification_model = ClassificationDeepLearningModel.objects.filter(task=last_added_task)[0].classification_model

    if request.method == 'POST':
        print("training should start now!")
        try:
            run_training(bucket_name="neurify-bucket", username=request.user.username, task_name=last_added_task.task_name)
        except:
            print("Could not run training!")
        else:
            print("training has finished!")
            context = {'done': 'done'}
            return redirect(reverse('ImageClassificationApp:training_progress'))



    context = {'last_task': last_added_task, 'image_classes': image_classes,
               "class_to_images_dict": class_to_images_dict, 'classification_model': classification_model}

    return render(request, 'ImageClassificationApp/pretraining_summary.html', context=context)



@login_required(login_url='ImageClassificationApp:login_page')
def training_progress_and_result(request):

    return render(request, 'ImageClassificationApp/training_progress.html')



@login_required(login_url='ImageClassificationApp:login_page')
def history_page(request):

    return render(request, 'ImageClassificationApp/history_page.html')



