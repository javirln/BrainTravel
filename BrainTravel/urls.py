from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BrainTravel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signin/$', 'principal.views.viewsModel1.metodo1'),
    #Para indicar en las URLs un metodo que se encuentra dentro de un archivo .py
    # url(r'^<nombre_url>$', '<app>.<paquete>.<archivo>.<metodo>'),
    # url(r'^<nombre_url>$', 'principal.views.ViewsModel1.method1')
)
