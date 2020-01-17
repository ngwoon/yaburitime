from django.shortcuts import render
from django.template import loader
# Create your views here.
from datetime import datetime

def board(request):
    #template = loader.get_template('board/index.html')
    now = datetime.now()
    context = {
        'current_date': now
    }

    return render(request, 'board/otherhtml/index.html', context)
