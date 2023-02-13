from polls.authentications  import views  as views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup',views.signup , name='signup'),
    path('verify_otp',views.verify_otp , name='verify_otp'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),  
    path('login', views.MyTokenObtainPairView.as_view() , name='token_obtain_pair'), 

    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),]