from django.conf.urls import url
from . import views
urlpatterns = {
    url("^login$",views.login_check),
    url("^index$",views.index),
    url("^menus$",views.get_menu)
}