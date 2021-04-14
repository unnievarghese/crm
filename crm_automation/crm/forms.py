from django import forms
from crm.models import *
from django.contrib.auth.forms import UserCreationForm,User
from django.forms import ModelForm
from datetime import date

class councilor_creationform(UserCreationForm):

    class Meta():
        model=User         #builtin model
        fields=['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
        }

class siginform(forms.Form):
     username=forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class': 'form-control'}))
     password = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class': 'form-control'}))

class course_creation_form(ModelForm):

    class Meta():
        model=Courses
        fields='__all__'
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_duration': forms.TextInput(attrs={'class': 'form-control'}),
        }

class batch_creation_form(ModelForm):

    class Meta():
        model=Batch
        fields='__all__'
        widgets = {
            'batch_code': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_date': forms.DateInput(attrs={'class': 'form-control'}),
            'course_fee': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data=super().clean()
        fee=int(cleaned_data.get('course_fee'))
        batchdate=cleaned_data.get('batch_date')
        if fee<5000:
            msg='Please re-check the fee'
            self.add_error('course_fee',msg)

        if batchdate<=date.today():
            msg='please enter a future date'
            self.add_error('batch_date',msg)

class enquiry_creation_form(ModelForm):

    class Meta():
        model=Enquiry
        fields='__all__'
        widgets = {
            'enquiryid': forms.TextInput(attrs={'class': 'form-control'}),
            'studentname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'collegename': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'enquirydate': forms.DateInput(attrs={'class': 'form-control'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'councillor': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

        }
    def clean(self):
        cleaned_data=super().clean()
        followup_date=cleaned_data.get('followup_date')
        if followup_date<=date.today():
            msg='please enter a future date'
            self.add_error('followup_date',msg)

class admission_creation_form(ModelForm):

    class Meta():
        model=Admission
        fields='__all__'
        widgets = {
            'admission_no': forms.TextInput(attrs={'class': 'form-control'}),
            'enquiryid': forms.TextInput(attrs={'class': 'form-control'}),
            'coursefee': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'councillor': forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
        }

    def clean(self):
        cleaned_data=super().clean()
        fee=cleaned_data.get('coursefee')
        if fee<5000:
            msg='Please re-check the fee'
            self.add_error('coursefee',msg)

class payment_form(ModelForm):

    class Meta():
        model=Payment
        fields='__all__'
        widgets = {
            'admission_no': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control'}),
            'enquiryid': forms.TextInput(attrs={'class': 'form-control'}),
        }
