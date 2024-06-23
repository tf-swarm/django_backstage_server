from django.conf.urls import url
from . import views
urlpatterns = {
    url("^rights/(\w+)$",views.getAllRights),
    url("^roles$", views.getRoles),
    url("^roles/(\d+)$", views.getRoleById),
    url("^roles/(\d+)/rights/(\d+)$",views.deleteRoleRight),
    url("^roles/(\d+)/rights$",views.updateRoleRight),

}