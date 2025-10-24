from django.shortcuts import render

def home_page(request):
    return render(request, 'zoo_app/index.html')
