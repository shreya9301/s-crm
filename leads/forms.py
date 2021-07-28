from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms.fields import EmailField
from django.http import request
from .models import Lead,Agent,Category
User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email")
        field_classes = {'username': UsernameField,'email':EmailField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset = Agent.objects.none())

    def __init__(self,*args,**kwargs):
        request = kwargs.pop("request") #used pop function to pop out those extra kwargs as they aren't really a part of original function
        agents = Agent.objects.filter(organization = request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args,**kwargs)
        self.fields["agent"].queryset = agents 

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )