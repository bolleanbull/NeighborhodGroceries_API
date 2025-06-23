from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from .models import Resource






class ResourceFilter(FilterSet):


    class Meta: 
        model = Resource
        fields = {
            'name': ['icontains', 'istartswith', 'iexact'],
            'condition': ['iexact'],
            'day_price': ['gt', 'lt', 'exact'],
            'availabel': ['iexact', 'exact'],
            'description': ['icontains']


        }