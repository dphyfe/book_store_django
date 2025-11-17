"""Forms for user authentication and account management."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Address, PaymentMethod


class RegisterForm(UserCreationForm):
    """Form for user registration."""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class LoginForm(AuthenticationForm):
    """Form for user login."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class AddressForm(forms.ModelForm):
    """Form for adding/editing addresses."""

    class Meta:
        model = Address
        fields = ["label", "address_line1", "address_line2", "city", "state", "zip_code", "is_default"]
        widgets = {
            "label": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Home, Work"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street Address"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apt, Suite, etc. (optional)"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "ZIP Code"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PaymentMethodForm(forms.ModelForm):
    """Form for adding payment methods."""

    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "1234 5678 9012 3456"}))
    cvv = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "CVV"}))

    class Meta:
        model = PaymentMethod
        fields = ["card_type", "cardholder_name", "expiry_month", "expiry_year", "is_default"]
        widgets = {
            "card_type": forms.Select(attrs={"class": "form-select"}),
            "cardholder_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name on Card"}),
            "expiry_month": forms.NumberInput(attrs={"class": "form-control", "placeholder": "MM", "min": 1, "max": 12}),
            "expiry_year": forms.NumberInput(attrs={"class": "form-control", "placeholder": "YYYY", "min": 2025}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        payment_method = super().save(commit=False)
        # Only save last 4 digits of card number
        card_number = self.cleaned_data["card_number"].replace(" ", "")
        payment_method.card_last_four = card_number[-4:]
        if commit:
            payment_method.save()
        return payment_method
