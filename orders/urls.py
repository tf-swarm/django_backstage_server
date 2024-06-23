from django.conf.urls import url
from . import views
urlpatterns = {
    url("^orders$",views.getAllOrder),
    url("^kuaidi/(\d+)$",views.getkuaidi),
    url("^reports/type/(\d+)$",views.statis),
}