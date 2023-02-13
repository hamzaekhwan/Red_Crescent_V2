
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/authentications/', include('polls.authentications.urls')),
    path('polls/reservations/', include('polls.reservations.urls')),
    path('polls/user_query/', include('polls.user_query.urls')),
    path('polls/user_requests/', include('polls.user_requests.urls')),
    path('polls/', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)