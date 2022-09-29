from django import forms


class ContactCreateForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea, help_text='Write your problem')
