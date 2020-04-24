from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Ad, Category, Message, Conversation


class ConversationForm(forms.Form):
    class Meta:
        model = Conversation


class ProfilForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(SignupForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control'
        })


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

TYPE_CHOICES = [
    ('supply', 'Offre'),
    ('demand', 'Demande'),
]

class AnnouncesForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea,required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    type = forms.CharField(
        required=True,
        widget=forms.Select(choices=TYPE_CHOICES),
    )

    def __init__(self, *args, **kwargs):
        super(AnnouncesForm,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['type'].widget.attrs.update({
            'class': 'form-control'
        })


    class Meta:
        model = Ad
        fields = ('title', 'description', 'category', 'type',)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),)


    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control'
        })


    class Meta:
        model = Ad
        fields = ('title', 'description', 'category', 'type',)

class MessageForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea)


    class Meta:
        model = Message
        fields = ('content',)