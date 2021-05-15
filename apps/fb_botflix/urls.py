from django.conf.urls import include, url
from .views import BotflixView
urlpatterns = [
    url(r'^6e92e34069be5fcb5df16172a9eb07020daccf76588baa9603/?$', BotflixView.as_view()) 
]