from django import forms
from store import models


class CustomerForm(forms.ModelForm):
  class Meta:
    model = models.Customer
    fields = '__all__'

  pass

class UserForm(forms.ModelForm):
  class Meta:
    model = models.User
    fields = ['first_name', 'last_name', 'username', 'email', 'password', 'user_role', 'is_active']

  pass

class ProductForm(forms.ModelForm):
  class Meta:
    model = models.Product
    fields = '__all__'

  pass

class SaleForm(forms.ModelForm):
  class Meta:
    model = models.Sale
    fields = '__all__'

  pass

class SaleItemForm(forms.ModelForm):
  class Meta:
    model = models.SaleItem
    fields = '__all__'

  pass
