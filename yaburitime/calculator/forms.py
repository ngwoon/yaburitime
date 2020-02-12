from django import forms


class Lessonform(forms.ModelForm):

    class Meta:
        fields = ('lesson_name', 'grade', 'credit',)