from django import forms
from .models import Feedback
from core.utils import DivErrorList

# a form to take in user feedback from the contact page
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = DivErrorList
