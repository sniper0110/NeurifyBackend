from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user

from .forms import UserForm

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


def home_page(request):

    return render(request, 'ImageClassificationApp/home.html')



def data_handling(request):

    return render(request, 'ImageClassificationApp/data_handling_page.html')



