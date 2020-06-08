from django.shortcuts import render

# Create your views here.

def login_page(request):

    return render(request, 'ImageClassificationApp/login_page.html')


def register_page(request):

    return render(request, 'ImageClassificationApp/register_page.html')



def home_page(request):

    return render(request, 'ImageClassificationApp/home.html')



def data_handling(request):

    return render(request, 'ImageClassificationApp/data_handling_page.html')



