from django import forms
from .models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        models = Seller
        fields ="__all__"
