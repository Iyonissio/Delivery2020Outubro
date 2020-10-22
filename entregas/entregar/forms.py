from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms
from .models import Order, Customer , Reserva , recomendacoes , Product , Room , Booking, Lotacao

class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])

class AddMesasForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class LotacaoForm(ModelForm):
    class Meta:
        model = Lotacao
        fields = '__all__'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['user']

class RecomendacoesForm(ModelForm):
    class Meta:
        model = recomendacoes
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']