from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.forms import inlineformset_factory


from .decorators import unauthenticated_user
from .forms import UserForm, TaskForm, ImageClassForm
from .models import Customer, Task, ImageClass

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


def home(request):

    return render(request, 'ImageClassificationApp/home.html')



def image_classification_content(request):

    TaskFormset = inlineformset_factory(Customer, Task, fields=('task_name',), extra=1)
    formset = TaskFormset(queryset=Task.objects.none(), instance=request.user.customer)

    if request.method == 'POST':

        formset = TaskFormset(request.POST, instance=request.user.customer)
        if formset.is_valid():
            saved_formset = formset.save()

            '''
            inst = someForm.customSave(request.user)
            inst.pk or inst.id
            '''
            return redirect(f'/home/image_classification/{saved_formset[0].pk}')

    context = {'formset':formset}
    return render(request, 'ImageClassificationApp/image_classification_content.html', context=context)




def image_classes_task(request, pk):

    task_from_pk = Task.objects.get(pk=pk)

    ImageClassFormset = inlineformset_factory(Task, ImageClass, fields=('image_classname',), extra=1)
    formset = ImageClassFormset(queryset=ImageClass.objects.none(), instance=task_from_pk)

    if request.method == 'POST':
        formset = ImageClassFormset(request.POST, instance=task_from_pk)
        if formset.is_valid():
            formset.save()
            return redirect(f'/home')

    context = {'formset': formset}
    return render(request, 'ImageClassificationApp/image_classes_form.html', context=context)


def data_handling(request):

    return render(request, 'ImageClassificationApp/data_handling_page.html')



