from django.conf.urls import url
from . import views
urlpatterns = {
    url("^users$",views.getAllUsers),
    url("^adduser$",views.createManager),
    url("^users/(\d+)/state/(\w+)$",views.updateActiveManager),
    url("^users/(\d+)$",views.updateManager),
}