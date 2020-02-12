from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
# Create your views here.
from datetime import datetime
from .models import Timetable, Lesson


def timetable_index(request):

    if request.user.is_anonymous:
        return redirect('/')

    if Timetable.objects.count() == 0:
        newtimetable = Timetable()
        newtimetable.table_name = '시간표1'
        newtimetable.user = request.user
        newtimetable.is_default = True
        newtimetable.save()

    timetables = Timetable.objects.filter(user=request.user).order_by('pk')
    print(timetables)
    default_table = Timetable.objects.filter(user=request.user, is_default=True).order_by('pk')

    context = {
        'timetables': timetables,
        'default_table': default_table,
    }
    return render(request, 'timetable/timetable_index.html', context)
