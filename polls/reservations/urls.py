from polls.reservations  import views  as views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('get_reservations',views.get_reservations , name='get_reservations'),
    path('valid_reservation',views.valid_reservation , name='valid_reservation'),
    path('reservepost',views.reservepost , name='reservepost'),
    ]


