from django.conf.urls import url
from hic.main import views

urlpatterns = [
     url(r'^', views.inicio, name='menu_principal'),
 ]