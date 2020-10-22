from django.shortcuts import render
from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from .models import *
from .forms import OrderForm , CreateUserForm , CustomerForm, ReservaForm , RecomendacoesForm, AddMesasForm,ProductForm, BookingForm, LotacaoForm
from .filters import OrderFilter , CustomerFilter, ReservaFilter, BookingFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user , allowed_users ,admin_only
from django.views.generic import ListView , FormView ,  View,  DeleteView
from .forms import AvailabilityForm
from django.urls import reverse, reverse_lazy


def check_availability(room, check_in, check_out):
    avail_list = []
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)


def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView', kwargs={
                           'category': room_category})

        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

    # def get_context_data(self, **kwargs):
    #     room = Room.objects.all()[0]
    #     room_categories = dict(room.ROOM_CATEGORIES)
    #     context = super().get_context_data(**kwargs)
    #     context


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        category = self.kwargs.get('category', None)

        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Categoria de Mesa nao Existe')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return render(request, 'booking_list_view.html')
        else:
            return render(request,'reservaIndisponivel.html')


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('BookingListView')





@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Conta criada com Sucesso para ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'entregar/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Nome de usuario ou password incorrecto!')

    context = {}
    return render(request, 'entregar/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def cozinha(request):
    orders = Order.objects.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders': orders,'myFilter': myFilter}
    return render(request, 'entregar/listapedidos.html', context)

@login_required(login_url='login')
@admin_only
def clientes(request):
    customers = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs
    context = {'customers':customers,'myFilter': myFilter}
    return render(request, 'entregar/listaclientes.html', context)

@login_required(login_url='login')
@admin_only
def listareservas(request):
    reservas = Booking.objects.all()
    myFilter = BookingFilter(request.GET, queryset=reservas)
    reservas = myFilter.qs
    context = {'reservas': reservas,'myFilter': myFilter}
    return render(request, 'entregar/listareservas.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    lot = Lotacao.objects.all()
    context = {'lot':lot}
    return render(request,'entregar/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    reservas = request.user.customer.reserva_set.all()
    lot = Lotacao.objects.all()
    context = {'reservas':reservas,'orders':orders,
               'lot': lot}
    return render(request, 'entregar/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userReservas(request):
    reservas = request.user.customer.reserva_set.all()

    context = {'reservas': reservas}
    return render(request, 'entregar/reservasuser.html', context)

@ login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def userPedidos(request):
    orders = request.user.customer.order_set.all()

    context = {'orders': orders}
    return render(request, 'entregar/pedidosuser.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accontSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'entregar/account_settings.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'products':products,}
    return render(request,'entregar/products.html',context)

def addproducts(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request,'entregar/addProductos.html', context)

def reports(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    reservas = Booking.objects.all()
    total_reservas = reservas.count()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Entregue').count()
    pending = orders.filter(status='Pendente').count()

    context = {'total_reservas': total_reservas, 'total_customers': total_customers,
               'reservas': reservas, 'orders': orders, 'customers': customers, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request,'entregar/reports.html', context)

def product_detail(request, pk_test):
    produ = Product.objects.get(id=pk_test)
    produtos = produ.order_set.all()
    context = {'produ': produ,'produtos': produtos}
    return  render(request,'entregar/product_detail.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count =orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'entregar/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'adicionar_Ingrediente','remover_Ingrediente','tipo_de_pedido'), extra=1)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'entregar/order_form.html', context)

def reserva(request, pk):
    ReservaFormSet = inlineformset_factory(Customer, Reserva,
    fields=('nome_da_reserva','mesas','entrada','saida','nr_de_pessoas'), extra=1)
    customer = Customer.objects.get(id=pk)
    formset = ReservaFormSet(queryset=Reserva.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = ReservaFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
        return redirect('/')
    context = {'formset': formset}
    return render(request, 'entregar/reserva.html', context)

def reclamacao(request):
    form = RecomendacoesForm()
    if request.method == 'POST':
        form = RecomendacoesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'entregar/reclamacao.html', context)

def AddMesas(request):
    form = AddMesasForm()
    if request.method == 'POST':
        form = AddMesasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'entregar/addMesas.html', context)

def AddMesas2(request):
    mesas = Room.objects.all()
    context = {'mesas': mesas}
    return render(request, 'entregar/addMesas2.html', context)


def updateReserva(request, pk):
    reserva = Booking.objects.get(id=pk)
    form = BookingForm(instance=reserva)
    if request.method == 'POST':
        form = BookingForm(request.POST , instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'entregar/actualizarReserva.html', context)

def deleteMesa(request, pk):
    reserva = Room.objects.get(id=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('/')

    context = {'reserva':reserva}
    return render(request, 'entregar/actualizarMesas.html', context)


def deleteReserva(request, pk):
    reserva = Booking.objects.get(id=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('/')

    context = {'reserva':reserva}
    return render(request, 'entregar/deleteReserva.html', context)

def createOrder2(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formsett = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formsett = OrderFormSet(request.POST, instance=customer)
        if formsett.is_valid():
            formsett.save()
            return redirect('/')
    context = {'formsett':formsett}
    return render(request, 'entregar/pedir.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','adminC'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST , instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'entregar/order_form2.html', context)

def updateLotacao(request):
    form = Lotacao.objects.all()
    if request.method == 'POST':
        form = LotacaoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'entregar/updateLotacao.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','adminC'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'entregar/delete.html', context)

