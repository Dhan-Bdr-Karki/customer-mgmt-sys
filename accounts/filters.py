from django.db.models import fields
import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):

    # Field lookup -> special name for actions on the field value you want to make when filtering data. 
    # e.g. lte, exact, icontains, iexact, contains,startswith, etc.
    # lookup _expr -> = '[Field lookup]'

    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']