from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from .views import home, Pativirakka, logIn, UserCreate, manage_authors, logOut

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('test/', manage_authors),
    path('login/', logIn, name='login'),
    path('logout/', logOut, name='logout'),
    path('pativirakka/', Pativirakka, name="pativirakka"),
    path('favicon.ico',
         RedirectView.as_view(url=staticfiles_storage.url('assets/img/favicon.ico')))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
