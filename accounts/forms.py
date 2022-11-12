from django.forms import ModelForm, fields
# In fact if your form is going to be used to directly add or edit a Django model, 
# a ModelForm can save you a great deal of time, effort, and code,
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order, Customer

# customer form
class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
    # Class Meta -> metadata options like get_latest_by, managed, order_with_respect_to, ordering, abstract
    # app_label, db_table etc.
    class Meta:
     
        model = Order   # which are in models.py 'room()'

        # all fields in the model should be used
        # can also be written as: fields = ['host','topic','name','description']
        fields = '__all__'
        
        # exclude = ['topic'] -> include all except excluded items


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']