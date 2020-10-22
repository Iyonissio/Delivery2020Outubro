from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('rooml', views.RoomListView, name='RoomListView'),
    path('booking_list/', views.BookingListView.as_view(), name='BookingListView'),
    path('room/<category>', views.RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', views.CancelBookingView.as_view(), name='CancelBookingView'),

    path('reports/', views.reports, name='reports'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accontSettings, name='account'),
    path('', views.home, name='home'),
    path('cozinha/', views.cozinha, name='cozinha'),
    path('userReservas/', views.userReservas, name='userReservas'),
    path('userPedidos/', views.userPedidos, name='userPedidos'),
    path('clientes/',views.clientes, name='clientes'),
    path('listareservas/', views.listareservas, name='listareservas'),
    path('products/', views.products,name='products'),
    path('addproducts/', views.addproducts,name='addproducts'),
    path('reclamacao/', views.reclamacao,name='reclamacao'),
    path('addmesa/', views.AddMesas,name='addmesa'),
    path('addmesa2/', views.AddMesas2, name='addmesa2'),
    path('product_detail/<int:pk_test>/', views.product_detail,name='product_detail'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('create_order/<str:pk>/', views.createOrder2, name='create_order2'),
    path('reserva/<str:pk>/', views.reserva, name='reserva'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('updateLotacao/', views.updateLotacao, name='updateLotacao'),


    path('update_reserva/<str:pk>/', views.updateReserva, name='update_reserva'),
    path('deletarMesa/<str:pk>/', views.deleteMesa, name='deletarMesa'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('delete_reserva/<str:pk>/', views.deleteReserva, name='delete_reserva'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='entregar/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='entregar/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='entregar/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='entregar/password_reset_done.html'),
         name='password_reset_complete'),
]
