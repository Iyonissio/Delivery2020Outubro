import django_filters
from django_filters import DateFilter , CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    #start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    #end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created','adicionar_Ingrediente','remover_Ingrediente']

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['name','email']

class ReservaFilter(django_filters.FilterSet):
    class Meta:
        model = Reserva
        fields = ['nome_da_reserva','nr_de_pessoas']

class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = ['user','room']
