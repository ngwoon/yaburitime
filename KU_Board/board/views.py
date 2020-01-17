from django.shortcuts import render
from django.template import loader
# Create your views here.
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


def board(request):
    #template = loader.get_template('board/index.html')
    now = datetime.now()
    context = {
        'current_date': now
    }
    return render(request, 'board/otherhtml/index.html', context)

def generic(request):
    return render(request, 'board/otherhtml/generic.html')

@csrf_exempt
def elements(request):
    return render(request, 'board/otherhtml/elements.html')