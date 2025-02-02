from django import forms
from . import models
from random import randrange, choice

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(choices=[("M","Male"),("F","Female"), ("Other","Other")], required=True)
    email_id = forms.EmailField(required=True)
    mobile_no = forms.CharField(required=True, min_length=10, max_length=10)
    college_name = forms.CharField(required=True)
    course = forms.CharField(required=True)
    city = forms.CharField(required=True)
    set_password = forms.CharField(required=True, min_length=6, widget=forms.PasswordInput())

    def save(self):
        try:
            user = models.CustomUser.objects.create(
                first_name = self.cleaned_data["full_name"],
                email = self.cleaned_data["email_id"],

                city = self.cleaned_data["city"],
                course = self.cleaned_data["course"],
                gender = self.cleaned_data["gender"],
                phone = self.cleaned_data["mobile_no"],
                college = self.cleaned_data["college_name"],
                username = self.generateUtkarshId()
            )
            user.set_password(self.cleaned_data["set_password"])
            user.save()
            return user
        except:
            raise forms.ValidationError("Error creating account")
    
    def clean_email_id(self):
        email = self.cleaned_data["email_id"]
        if models.CustomUser.objects.filter(email = email):
            raise forms.ValidationError("Email already registered.")
        return email
    
    def clean_mobile_no(self):
        phone = self.cleaned_data["mobile_no"]
        if len(phone) != 10 or phone[0] in ['0', '1', '2', '3', '4', '5']:
            raise forms.ValidationError("Invalid Mobile no.")
        return phone
    

    def generateUtkarshId(self):
        attempts = 0
        while True:
            # check if not exists
            attempts += 1
            if attempts > 5:
                i = "UK25" + choice(["U","T","K","A","R","S","H"]) + str(randrange(1000, 99999))
            i = "UK25" + str(randrange(100, 9999))
            if not models.CustomUser.objects.filter(username=i).exists():
                return i





class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.CustomUser
        fields = ("username","password","email")


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = models.CustomUser
#         fields = ("username","password")