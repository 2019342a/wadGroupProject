from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static 
from registration.backends.simple.views import RegistrationView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^storyteller/', include('storyteller.urls')),
    # url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    # (r'^accounts/', include('registration.backends.simple.urls')),
)
