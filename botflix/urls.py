# url's 
from django.conf.urls import url, include
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fb_botflix/', include('apps.fb_botflix.urls')),
]

