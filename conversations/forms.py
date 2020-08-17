from django import forms
from .models import Message, Conversation
from users.models import User


class MessageForm(forms.Form):
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write message here",
                "class": "w-4/5 h-20 border p-3",
            }
        ),
    )
