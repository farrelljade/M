from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    """Create a tweet body form."""
    class Meta:
        model = Tweet
        fields = ['body']  # Specify the fields to be used from the model
        widgets = {
            'body': forms.Textarea(
                attrs={
                    "placeholder": "Enter your Tweet!",
                    "class": "form-control",
                }
            ),
        }
        labels = {
            'body': '',  # Hides the label for the body field
        }
