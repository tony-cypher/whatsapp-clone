from django import forms
from .models import GroupMessage

class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message', 'id': 'message-input'})
        }