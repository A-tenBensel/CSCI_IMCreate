from django import forms
from apps.comments.models import Comment

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'text_example': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter task name',
            }),
            'number_example': forms.NumberInput(attrs={
                'min': 1, 'max': 10,
                'placeholder': '1-10',
            }),
            'date_example': forms.DateInput(attrs={
                'type': 'date'
            }),
            'time_example': forms.TimeInput(attrs={
                'type': 'time'
            }),
        }