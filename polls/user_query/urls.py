from polls.user_query  import views  as views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('count_shift_post',views.count_shift_post , name='count_shift_post'),
    path('myreservations',views.myreservations , name='myreservations'),
    ]
