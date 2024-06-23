from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url("^categories$", views.getAllCategories),
    url("^categories/(\d+)$", views.catManage),
    url("^categories/(\d+)/attributes$", views.getAttributes),
    url("^categories/(\d+)/attributes/(\d+)$", views.attrManage),
    url("^goods$",views.getAllGoods),
    url("^goods/(\d+)$",views.goodsManage),
    url("^upload$", views.upload),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
