from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy

class Mesas (models.Model):
    MESAS_CATEGORIA = (
        ('EMPRESARIAL', 'EMPRESARIAL'),
        ('SOCIAL', 'SOCIAL'),
        ('CASAL', 'CASAL'),
    )
    numero = models.IntegerField()
    categoria = models.CharField(max_length=15, choices=MESAS_CATEGORIA)
    cadeiras =models.IntegerField()
    capacidade = models.IntegerField()

    def __str__(self):
        return f'{self.numero}.   com  {self.cadeiras}  Cadeiras  para  {self.capacidade}  Pessoas  '

class Room(models.Model):
    ROOM_CATEGORIES = (
        ('EMPRESARIAL', 'EMPRESARIAL'),
        ('SOCIAL', 'SOCIAL'),
        ('CASAL', 'CASAL'),
        ('VIP','VIP')
    )
    number = models.IntegerField()
    category = models.CharField(max_length=15, choices=ROOM_CATEGORIES)
    cadeiras = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.number}. {dict(self.ROOM_CATEGORIES)[self.category]} Cadeiras = {self.cadeiras} Pessoas = {self.capacity}'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'

    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category

    def get_cancel_booking_url(self):
        return reverse_lazy('CancelBookingView', args=[self.pk, ])


class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank= True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="Prato_2",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.phone

    def __str__(self):
        return str(self.user)

class Reserva (models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    mesas = models.ForeignKey(Mesas, null=True,on_delete=models.CASCADE)
    entrada = models.DateTimeField()
    saida = models.DateTimeField()
    nome_da_reserva = models.CharField(max_length=200, null=True)
    nr_de_pessoas = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer} efectuou reserva com sucesso na mesa {self.mesas} duracao de {self.entrada} ate {self.saida}'


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Promocao do Dia', 'Promocao do Dia'),
        ('Preco Normal', 'Preco Normal')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField( null=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.TextField(max_length=134500, null=True, blank= True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="SemFT.png",null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    STATUS = (
        ('Pendente', 'Pendente'),
        ('Pronto em 30min', 'Pronto em 30min'),
        ('Pronto em 15min', 'Pronto em 15min'),
        ('Pronto em 5min', 'Pronto em 5min'),
        ('Saiu Para Entrega', 'Saiu Para Entrega'),
        ('Entregue', 'Entregue'),
    )
    TIPO_DE_PEDIDO = (
        ('RECEBER ENCASA','RECEBER ENCASA'),
        ('COMER NO RESTAURANTE', 'COMER NO RESTAURANTE'),
        ('LEVANTAR PESSOALMENTE', 'LEVANTAR PESSOALMENTE'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    adicionar_Ingrediente = models.CharField(max_length=200, null=True)
    remover_Ingrediente = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    tipo_de_pedido = models.CharField(max_length=200, null=True, choices=TIPO_DE_PEDIDO)

    def __str__(self):
        return self.product.name

class recomendacoes(models.Model):
    reclamacao = models.TextField(blank=True,null=True, max_length=5000)
    recomendacao = models.TextField(blank=True, null=True, max_length=5000)

    def __str__(self):
        return 'Reclamacao: '+self.reclamacao+' Recomendacao: '+self.recomendacao

class Lotacao(models.Model):
    numero_de_clientes = models.CharField(blank=True, null=True, max_length=50)
    capacidade = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return f'{self.numero_de_clientes}'

    def __str__(self):
        return f'{self.capacidade}'
