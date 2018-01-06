from django.conf.urls import url
from . import views        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^regis$', views.regis),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^wish_items/create$', views.createitems),
    url(r'^add/(?P<itemid>\d+)$', views.addtolist),
    url(r'^remove/(?P<itemid>\d+)$', views.remove),
    url(r'^delete/(?P<itemid>\d+)$', views.delete),
    url(r'^wish_items/(?P<itemid>\d+)$', views.showitem),
    ]
