from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import home, Pativirakka, logIn, UserCreate, manage_authors, logOut

urlpatterns = [
    path('', home, name='home'),
    path('login/', logIn, name='login'),
    path('logout/', logOut, name='logout'),
    path('signup/', UserCreate.as_view(), name='signup'),
    path('pativirakka/', Pativirakka, name="pativirakka"),
    path('data/', manage_authors, name="data"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
