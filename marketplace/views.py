from django.shortcuts import render, redirect, get_object_or_404




def home(request):
    return render(request, 'main/home.html')
