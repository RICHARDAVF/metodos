from django.urls import path
from .views import index,hermite
urlpatterns = [
    path("",index),
    path("hermite",hermite,name="method_hermite")
]