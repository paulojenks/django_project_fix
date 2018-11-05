from django.conf.urls import url
from menu import views


app_name = "menu"
urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/new/$', views.menu_new, name='menu_new'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.menu_edit, name='menu_edit'),
    url(r'^menu/item/$', views.item_list, name='item_list'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
]
