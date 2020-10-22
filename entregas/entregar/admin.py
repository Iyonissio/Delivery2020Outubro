from django.contrib import admin
from .models import Customer , Product , Order, Tag , Reserva , recomendacoes , Mesas, Room, Booking, Lotacao

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(Reserva)
admin.site.register(recomendacoes)
admin.site.register(Mesas)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Lotacao)


