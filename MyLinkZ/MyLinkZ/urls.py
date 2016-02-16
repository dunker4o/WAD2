from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyLinkZ.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^Rango/', include('Rango.urls')),
	url(r'^secret/', include('Rango.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('django.views.static',(r'^media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}), )