from polls.user_requests  import views  as views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('reservepost_cancel',views.reservepost_cancel , name='reservepost_cancel'),
    path('reservepost_repair',views.reservepost_repair , name='reservepost_repair'),
    path('query_about_cancel',views.query_about_cancel , name='query_about_cancel'),
    path('query_about_repair',views.query_about_repair , name='query_about_repair'),
    ]