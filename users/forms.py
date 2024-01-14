from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from users.models import User


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={
        "placeholder": "Enter First Name", 
        "id":"fname", 
        }),
    )
    last_name = forms.CharField(
        required=False,
        max_length=255, 
        widget=forms.TextInput(attrs={
        "placeholder": "Enter Last Name",
        "id": "lname",
        })
    )
    email = forms.EmailField(
        required=False,
        max_length=200,
        widget=forms.EmailInput(attrs={
        "placeholder": "Enter Your Email",
        "id": "email"
        }),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].help_text = "Required. Valid email address"

        self.fields["password1"].widget = forms.PasswordInput(
            
            attrs={
            
            "placeholder": _("Create Password"),
            "id": _("password1")
            },
            
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
            "placeholder": _("Confirm Password"),
            "id": _("password2")
            },
           
        )
       
        for fieldname in ["first_name", "last_name", "email", "password1", "password2"]:
            self.fields[fieldname].label = ""


class UserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=200,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter First Name"}),
    )
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Valid Email Address"}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
