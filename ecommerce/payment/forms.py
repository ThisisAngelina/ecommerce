from django import forms

from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'street_name_number', 'city', 'country', 'zip_code']
        exclude = ('user', ) # N.B. must be a tuple