from django.shortcuts import render
from django.shortcuts import redirect
from .forms import Lessonform


def calculator(request):

    return render(request, 'calculator/calculator.html')